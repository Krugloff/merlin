class HtmlSpellTest < Test::Unit::TestCase
  # Casting
  def self.pretty(html)
    html.gsub( /^ {4,4}/, '' ).gsub( /\n\n/, "\n  \n" )
  end

  HTML = pretty <<-HTML
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

  test 'should cast text template' do
    spell = Merlin::HtmlSpell.new <<-TEMPLATE
      doctype!
      html do
        head do
          link rel: 'stylesheet', href: 'style.css'
          script src: 'jquery.js'
        end

        body :id => :frontpage do
          h1 'Hello World', :class => :main
        end
      end
    TEMPLATE

    assert_equal HTML, spell.cast
  end

  test 'should render block template' do
    spell = Merlin::HtmlSpell.new do
      doctype!
      html do
        head do
          link rel: 'stylesheet', href: 'style.css'
          script src: 'jquery.js'
        end

        body :id => :frontpage do
          h1 'Hello World', :class => :main
        end
      end
    end

    assert_equal HTML, spell.cast
  end

  ##### Artefacts
  test 'should init vars from args' do
    spell = Merlin::HtmlSpell.new(spell: 'Abracadabra!') { text @spell }
    effect = spell.cast

    assert_equal 'Abracadabra!', effect
  end

  test 'should init vars from context object' do
    ( context = Object.new ).instance_variable_set :@spell, 'Abracadabra!'
    spell = Merlin::HtmlSpell.new(context) { text @spell }
    effect = spell.cast

    assert_equal 'Abracadabra!', effect
  end

  test 'should send missing method to context' do
    ( context = Object.new ).define_singleton_method(:spell) { 'Abracadabra!' }
    effect = Merlin::HtmlSpell.new(context) { text spell }.cast

    assert_equal 'Abracadabra!', effect
  end
end
