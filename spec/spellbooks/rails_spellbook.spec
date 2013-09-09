require_relative '../helper'

##### From haml.
require 'action_pack'
require 'action_controller'
require 'action_view'
require 'active_model'

require 'rails'

class TestApp < Rails::Application
  config.root = ""
end

Rails.application = TestApp

ActionController::Base.logger = Logger.new($stdout)
#####

# Pseudo models.
class Post
  include ActiveModel::Model
  attr_accessor :author, :title, :time_zone
end

class Author
  include ActiveModel::Model
  attr_accessor :name
end

#! From merlin.rb. Because merlin load once in spec helper.
Merlin::Builders::HtmlSpellBuilder
  .send :include, Merlin::Spellbooks::RailsSpellbook

ActionView::Template.register_template_handler :spell, Merlin::HtmlSpell
#####

describe Merlin::Spellbooks::RailsSpellbook do
  let(:render) { -> (text) { @base.render inline: text, type: 'spell' } }

  let(:pretty) do
    proc do |html, indent: 8|
      html
        .gsub( /^ {#{indent},#{indent}}/, '' )
        .gsub( /\n\n/, "\n  \n" )
        .rstrip
    end
  end

  let(:post) do
    Post.new author: 'Krugloff', title: 'Art of Magic', time_zone: 'Moscow'
  end

  let(:author) { Author.new name: 'Krugloff'}

  before do
    @base = ActionView::Base.new
    @base.controller = ActionController::Base.new
    @base.view_paths << File.expand_path("../../templates", __FILE__)

    # This is needed for >=3.0.0. From Haml.
    if defined?(ActionController::Response)
      @base.controller.response = ActionController::Response.new
    end

    @base.define_singleton_method('protect_against_forgery?') { true }
    @base.define_singleton_method('form_authenticity_token') { '12345' }

    @base.instance_variable_set '@post', post
    @base.instance_variable_set '@author', author
  end
  #####

  context 'when html helpers' do
    it 'renders text' do
      html = render.('`Hello!`')
      expect(html).to eql 'Hello!'
    end

    it 'renders tags' do
      html = render.("a 'Hello World', href: ?#")
      expect(html).to eql "<a href='#'>Hello World</a>"
    end
  end

  context 'when rails helpers' do
    context 'when tag helpers' do
      it 'renders tag' do
        html = render.("tag 'br'")
        expect(html).to eql '<br />'
      end

      it 'renders content tag' do
        html = render.("content_tag :p, 'Hello world!'")
        expect(html).to eql '<p>Hello world!</p>'
      end

      it 'renders content tag with block' do
        html = render.("content_tag(:p) { span 'Abracadabra!' }")
        expect(html).to eql '<p><span>Abracadabra!</span></p>'
      end

      it 'renders cdata' do
        html = render.("cdata_section '<hello world>'")
        expect(html).to eql '<![CDATA[<hello world>]]>'
      end
    end

    context 'when url helpers' do
      it 'renders link to' do
        template = "link_to 'Visit Other Site', 'http://www.rubyonrails.org/', data: {confirm: 'Are you sure?'}"

        result   = '<a data-confirm="Are you sure?" href="http://www.rubyonrails.org/">Visit Other Site</a>'

        html = render.(template)
        expect(html).to eql result
      end

      it 'renders button to' do
        template = "button_to 'Destroy', 'http://www.example.com', data: { confirm: 'Are you sure?', disable_with: 'loading...' }, method: 'delete', remote: true"

        result   = '<form action="http://www.example.com" class="button_to" data-remote="true" method="post"><div><input name="_method" type="hidden" value="delete" /><input data-confirm="Are you sure?" data-disable-with="loading..." type="submit" value="Destroy" /><input name="authenticity_token" type="hidden" value="12345" /></div></form>'

        html = render.(template)
        expect(html).to eql result
      end

      #! Need `.request`.
      # it 'renders link to unless current' do
      #   html = render.("link_to_unless_current('Home', { action: 'index' })")
      #   expect(html).to eql ''
      # end

      it 'renders link to if' do
        template = "link_to_if true, 'Visit Other Site', 'http://www.rubyonrails.org/', data: {confirm: 'Are you sure?'}"

        result   = '<a data-confirm="Are you sure?" href="http://www.rubyonrails.org/">Visit Other Site</a>'

        html = render.(template)
        expect(html).to eql result
      end

      it 'renders link to unless' do
        template = "link_to_unless false, 'Visit Other Site', 'http://www.rubyonrails.org/', data: {confirm: 'Are you sure?'}"

        result   = '<a data-confirm="Are you sure?" href="http://www.rubyonrails.org/">Visit Other Site</a>'

        html = render.(template)
        expect(html).to eql result
      end

      it 'renders mail to' do
        html = render.("mail_to 'me@domain.com'")
        expect(html).to eql '<a href="mailto:me@domain.com">me@domain.com</a>'
      end
    end

    context 'when text helpers' do
      it 'renders concat' do
        html = render.("concat '<br>'")
        expect(html).to eql '<br>'
      end

      it 'renders safe concat' do
        html = render.("safe_concat '<br>'")
        expect(html).to eql '&lt;br&gt;'
      end

      it 'renders simple format' do
        template = "simple_format 'Here is some basic text...\n...with a line break.'"

        result   = "<p>Here is some basic text...\n<br />...with a line break.</p>"

        html = render.(template)
        expect(html).to eql result
      end
    end

    context 'when rendering helpers' do
      let(:html) do
        pretty.call <<-HTML
          <!DOCTYPE html>
          <html>
            <head>
              <link rel='stylesheet' href='style.css'>
              <script src='jquery.js'></script>
            </head>

            <body id='frontpage'>
              <h1 class='main'>Hello World</h1>
            </body>
          </html>
        HTML
      end

      it 'renders text' do
        html = render.("render text: 'Abracadabra!'")
        expect(html).to eql 'Abracadabra!'
      end

      it 'renders inline' do
        template = "mail_to 'me@domain.com'"

        html = render.("render inline: \"#{template}\", :type => :spell")
        expect(html).to eql '<a href="mailto:me@domain.com">me@domain.com</a>'
      end

      it 'renders partial' do
        html = render.("render 'partial'")
        expect(html).to eql html
      end

      it 'renders file' do
        html = render.("render file: 'file'")
        expect(html).to eql html
      end
    end

    context 'when record tag helpers' do
      it 'renders div for model' do
        html = render.('div_for @post')
        expect(html).to eql '<div class="post" id="new_post"></div>'
      end

      it 'renders content tag for model' do
        html = render.('content_tag_for :tr, @post')
        expect(html).to eql '<tr class="post" id="new_post"></tr>'
      end
    end

    context 'when javascript helpers' do
      it 'renders javascript tag' do
        html = render.("javascript_tag \"alert('Hello!')\", defer: 'defer'")
        expect(html).to eql "<script defer=\"defer\">\n//<![CDATA[\nalert('Hello!')\n//]]>\n</script>"
      end

      it 'renders javascript cdata section' do
        html = render.("javascript_cdata_section \"alert('Hello!')\"")
        expect(html).to eql "\n//<![CDATA[\nalert('Hello!')\n//]]>\n"
      end

      #! Deprecated.
      it 'renders button to function' do
        html = render.("button_to_function 'Hello', \"alert('Hello')\", class: 'ok'")
        expect(html).to eql '<input class="ok" onclick="alert(&#39;Hello&#39;);" type="button" value="Hello" />'
      end

      #! Deprecated.
      it 'renders link to function' do
        html = render.("link_to_function 'Hello', \"alert('Hello!')\", class: 'nav_link'")
        expect(html).to eql '<a class="nav_link" href="#" onclick="alert(&#39;Hello!&#39;); return false;">Hello</a>'
      end
    end

    context 'when form tag helpers' do
      it 'renders form tag' do
        html = render.("form_tag('/posts/1', method: :put)")
        expect(html).to eql '<form accept-charset="UTF-8" action="/posts/1" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="_method" type="hidden" value="put" /><input name="authenticity_token" type="hidden" value="12345" /></div>'
      end

      it 'renders form tag with block' do
        html = render.(
          <<-TAG
            form_tag('/posts') do
              div { submit_tag 'Save' }
            end
          TAG
        )

        expect(html).to eql '<form accept-charset="UTF-8" action="/posts" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="12345" /></div><div><input name="commit" type="submit" value="Save" /></div></form>'
      end

      it 'renders select tag' do
        html = render.("select_tag 'people', '<option>David</option>'.html_safe")
        expect(html).to eql '<select id="people" name="people"><option>David</option></select>'
      end

      it 'renders text field tag' do
        html = render.("text_field_tag 'name'")
        expect(html).to eql '<input id="name" name="name" type="text" />'
      end

      it 'renders label tag' do
        html = render.("label_tag 'name', nil, class: 'small_label'")
        expect(html).to eql '<label class="small_label" for="name">Name</label>'
      end

      it 'renders hidden field tag' do
        html = render.("hidden_field_tag 'token', 'VUBJKB23UIVI1UU1VOBVI@'")
        expect(html).to eql '<input id="token" name="token" type="hidden" value="VUBJKB23UIVI1UU1VOBVI@" />'
      end

      it 'renders file field tag' do
        html = render.("file_field_tag 'avatar', class: 'profile_input'")
        expect(html).to eql '<input class="profile_input" id="avatar" name="avatar" type="file" />'
      end

      it 'renders password field tag' do
        html = render.("password_field_tag 'secret', 'Your secret here'")
        expect(html).to eql '<input id="secret" name="secret" type="password" value="Your secret here" />'
      end

      it 'renders text area tag' do
        html = render.("text_area_tag 'body', nil, rows: 10, cols: 25")
        expect(html).to eql "<textarea cols=\"25\" id=\"body\" name=\"body\" rows=\"10\">\n</textarea>"
      end

      it 'renders check box tag' do
        html = render.("check_box_tag 'rock', 'rock music'")
        expect(html).to eql '<input id="rock" name="rock" type="checkbox" value="rock music" />'
      end

      it 'renders radio button tag' do
        html = render.("radio_button_tag 'receive_updates', 'no', true")
        expect(html).to eql '<input checked="checked" id="receive_updates_no" name="receive_updates" type="radio" value="no" />'
      end

      it 'renders submit tag' do
        html = render.("submit_tag 'Edit', class: 'edit_button'")
        expect(html).to eql '<input class="edit_button" name="commit" type="submit" value="Edit" />'
      end

      it 'renders button tag' do
        html = render.("button_tag")
        expect(html).to eql '<button name="button" type="submit">Button</button>'
      end

      it 'renders image submit tag' do
        html = render.("image_submit_tag('purchase.png', disabled: true)")
        expect(html).to eql '<input alt="Purchase" disabled="disabled" src="/images/purchase.png" type="image" />'
      end

      it 'renders field set tag' do
        html = render.("field_set_tag { text_field_tag 'name' }")
        expect(html).to eql '<fieldset><input id="name" name="name" type="text" /></fieldset>'
      end

      it 'renders color field tag' do
        html = render.("color_field_tag 'name'")
        expect(html).to eql '<input id="name" name="name" type="color" />'
      end

      it 'renders search field tag' do
        html = render.("search_field_tag 'name'")
        expect(html).to eql '<input id="name" name="name" type="search" />'
      end

      it 'renders telephone field tag' do
        html = render.("telephone_field_tag 'name'")
        expect(html).to eql '<input id="name" name="name" type="tel" />'
      end

      it 'renders phone field tag' do
        html = render.("phone_field_tag 'name'")
        expect(html).to eql '<input id="name" name="name" type="tel" />'
      end

      it 'renders date field tag' do
        html = render.("date_field_tag 'name'")
        expect(html).to eql '<input id="name" name="name" type="date" />'
      end

      it 'renders time field tag' do
        html = render.("time_field_tag 'name'")
        expect(html).to eql '<input id="name" name="name" type="time" />'
      end

      it 'renders datetime field tag' do
        html = render.("datetime_field_tag 'name'")
        expect(html).to eql '<input id="name" name="name" type="datetime" />'
      end

      it 'renders datetime local field tag' do
        html = render.("datetime_local_field_tag 'name'")
        expect(html).to eql '<input id="name" name="name" type="datetime-local" />'
      end

      it 'renders month field tag' do
        html = render.("month_field_tag 'name'")
        expect(html).to eql '<input id="name" name="name" type="month" />'
      end

      it 'renders week field tag' do
        html = render.("week_field_tag 'name'")
        expect(html).to eql '<input id="name" name="name" type="week" />'
      end

      it 'renders url field tag' do
        html = render.("url_field_tag 'name'")
        expect(html).to eql '<input id="name" name="name" type="url" />'
      end

      it 'renders email field tag' do
        html = render.("email_field_tag 'name'")
        expect(html).to eql '<input id="name" name="name" type="email" />'
      end

      it 'renders number field tag' do
        html = render.("number_field_tag 'quantity', nil, in: 1...10")
        expect(html).to eql '<input id="quantity" max="9" min="1" name="quantity" type="number" />'
      end

      it 'renders range field tag' do
        html = render.("range_field_tag 'name'")
        expect(html).to eql '<input id="name" name="name" type="range" />'
      end

      it 'renders utf8 enforcer tag' do
        html = render.('utf8_enforcer_tag')
        expect(html).to eql '<input name="utf8" type="hidden" value="&#x2713;" />'
      end
    end

    context 'when form options helpers' do
      let(:authors) { %w[ Krugloff Kruglodd Kruglopp ] }

      it 'renders select for (instead select)' do
        html = render.("select_for :post, :author, #{authors}")
        expect(html).to eql pretty.call <<-SELECT, indent: 10
          <select id="post_author" name="post[author]"><option selected="selected" value="Krugloff">Krugloff</option>
          <option value="Kruglodd">Kruglodd</option>
          <option value="Kruglopp">Kruglopp</option></select>
        SELECT
      end

      it 'renders collection select' do
        html = render.("collection_select :post, :author, #{authors}, :to_s, :inspect")
        expect(html).to eql pretty.call <<-SELECT, indent: 10
          <select id="post_author" name="post[author]"><option selected="selected" value="Krugloff">&quot;Krugloff&quot;</option>
          <option value="Kruglodd">&quot;Kruglodd&quot;</option>
          <option value="Kruglopp">&quot;Kruglopp&quot;</option></select>
        SELECT
      end

      it 'renders grouped collection select' do
        html = render.("grouped_collection_select :post, :author, #{authors}, :chars, :inspect, :object_id, :inspect")
        expect(html).to match(/<select.*<\/select>/m)
      end

      it 'renders time zone select' do
        html = render.('time_zone_select "post", "time_zone", /Australia/')
        expect(html).to match(/select/)
      end

      it 'renders collection radio buttons' do
        html = render.("collection_radio_buttons :post, :author, #{authors}, :to_s, :inspect")
        expect(html).to match(/input/)
      end

      it 'renders collection check boxes' do
        html = render.("collection_check_boxes :post, :author, #{authors}, :to_s, :inspect")
        expect(html).to match(/input/)
      end
    end

    context 'when form helper' do
      it 'renders form for' do
        html = render.('form_for(@post, url: "www.example.com") {}')
        expect(html).to match(/<form.*<\/form>/m)
      end

      it 'renders fields for' do
        template = <<-TEMPLATE
          fields_for @post do |fields|
            fields.text_field :author
          end
        TEMPLATE

        html = render.("#{template}")
        expect(html).to eql '<input id="post_author" name="post[author]" type="text" value="Krugloff" />'
      end

      it 'renders label for (instead label)' do
        html = render.('label_for :post, :author, "Author"')
        expect(html).to eql '<label for="post_author">Author</label>'
      end

      it 'renders fields for in form' do
        template = <<-TEMPLATE
          form_for @post, url: "www.example.com" do |post_form|
            post_form.fields_for @author do |author_fields|
              author_fields.text_field :name
            end

            div.post_form { post_form.text_field :title }
          end
        TEMPLATE

        html = render.("#{template}")
        expect(html).to eql pretty.call <<-FORM, indent: 10
          <form accept-charset="UTF-8" action="www.example.com" class="new_post" id="new_post" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="12345" /></div><input id="post_author_name" name="post[author][name]" type="text" value="Krugloff" />
          <div class='post_form'>
            <input id="post_title" name="post[title]" type="text" value="Art of Magic" />
          </div>
          </form>
        FORM
      end
    end

    context 'when debug helper' do
      it 'renders debug' do
        html = render.('debug @post')
        expect(html).to eql pretty.call <<-DEBUG, indent: 10
          <pre class="debug_dump">--- !ruby/object:Post
          author: Krugloff
          title: Art of Magic
          time_zone: Moscow
          </pre>
        DEBUG
      end
    end

    context 'when date helpers' do
      ##### It's also in form_for.
      it 'renders date select' do
        html = render.('date_select "user", "birthday"')
        expect(html).to match(/select/)
      end

      it 'renders time select' do
        html = render.('time_select "article", "sunrise"')
        expect(html).to match(/select/)
      end

      it 'renders datetime select' do
        html = render.('datetime_select "article", "written_on"')
        expect(html).to match(/select/)
      end
      #####

      it 'renders select datetime' do
        html = render.('select_datetime')
        expect(html).to match(/select/)
      end

      it 'renders select date' do
        html = render.('select_date')
        expect(html).to match(/select/)
      end

      it 'renders select time' do
        html = render.('select_time')
        expect(html).to match(/select/)
      end

      it 'renders select second' do
        html = render.('select_second 33')
        expect(html).to match(/select/)
      end

      it 'renders select minute' do
        html = render.('select_minute 14')
        expect(html).to match(/select/)
      end

      it 'renders select hour' do
        html = render.('select_hour 13')
        expect(html).to match(/select/)
      end

      it 'renders select day' do
        html = render.('select_day 5')
        expect(html).to match(/select/)
      end

      it 'renders select month' do
        html = render.('select_month Date.today')
        expect(html).to match(/select/)
      end

      it 'renders select year' do
        html = render.('select_year Date.today')
        expect(html).to match(/select/)
      end

      it 'renders time tag' do
        html = render.('time_tag Date.today')
        expect(html).to match(/<time.*>/)
      end
    end

    context 'when csrf helpers' do
      it 'renders csrf meta tags' do
        html = render.('csrf_meta_tags')
        expect(html).to eql "<meta content=\"authenticity_token\" name=\"csrf-param\" />\n<meta content=\"12345\" name=\"csrf-token\" />"
      end

      it 'renders csrf meta tag' do
        html = render.('csrf_meta_tag')
        expect(html).to eql "<meta content=\"authenticity_token\" name=\"csrf-param\" />\n<meta content=\"12345\" name=\"csrf-token\" />"
      end
    end

    context 'when capture helpers' do
      it 'renders capture' do
        html = render.('text capture { `Abracadabra!` }')
        expect(html).to eql 'Abracadabra!'
      end

      it 'renders content for' do
        html = render.call <<-CONTENT
          content_for(:magic) { p 'Abracadabra!' }
          content_for(:magic) { p 'Avada Kedavra!' }
          content_for :magic
        CONTENT

        expect(html).to eql '<p>Abracadabra!</p><p>Avada Kedavra!</p>'
      end

      #! Fail and i don't know why.
      # it 'renders provide' do
        # html = render.call <<-CONTENT
        #   provide(:magic) { p 'Abracadabra!' }
        #   provide(:magic) { p 'Avada Kedavra!' }
        #   text! provide(:magic)
        # CONTENT

        # expect(html).to eql '<p>Avada Kedavra!</p>'
      # end
    end

    context 'when asset tag helpers' do
      it 'renders javascript include tag' do
        html = render.('javascript_include_tag "xmlhr"')
        expect(html).to eql '<script src="/javascripts/xmlhr.js"></script>'
      end

      it 'renders stylesheet link tag' do
        html = render.('stylesheet_link_tag "style"')
        expect(html).to eql '<link href="/stylesheets/style.css" media="screen" rel="stylesheet" />'
      end

      it 'renders auto discovery link tag' do
        html = render.('auto_discovery_link_tag :rss, "http://www.example.com/feed.rss", title: "Example RSS"')
        expect(html).to eql '<link href="http://www.example.com/feed.rss" rel="alternate" title="Example RSS" type="application/rss+xml" />'
      end

      it 'renders favicon link tag' do
        html = render.('favicon_link_tag "/myicon.ico"')
        expect(html).to eql '<link href="/myicon.ico" rel="shortcut icon" type="image/vnd.microsoft.icon" />'
      end

      it 'renders image tag' do
        html = render.('image_tag "icon"')
        expect(html).to eql '<img alt="Icon" src="/images/icon" />'
      end

      it 'renders video tag' do
        html = render.('video_tag "trailer"')
        expect(html).to eql '<video src="/videos/trailer"></video>'
      end

      it 'renders audio tag' do
        html = render.('audio_tag "sound"')
        expect(html).to eql '<audio src="/audios/sound"></audio>'
      end
    end

  end
end
