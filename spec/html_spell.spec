require_relative 'helper'

describe Merlin::HtmlSpell do
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

  context 'when template' do
    it 'renders text' do
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

      expect(spell.cast).to eql HTML
    end

    it 'renders block' do
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

      expect(spell.cast).to eql HTML
    end
  end

  context 'when vars' do
    it 'inits vars' do
      spell = Merlin::HtmlSpell.new(spell: 'Abracadabra!') { text @spell }
      effect = spell.cast

      expect(effect).to eql 'Abracadabra!'
    end
  end

  context 'when context object' do
    it 'inits vars' do
      ( context = Object.new ).instance_variable_set :@spell, 'Abracadabra!'
      spell = Merlin::HtmlSpell.new(context) { text @spell }
      effect = spell.cast

      expect(effect).to eql 'Abracadabra!'
    end

    it 'sends missing method to context' do
      ( context = Object.new ).define_singleton_method(:spell) { 'Abracadabra!' }
      effect = Merlin::HtmlSpell.new(context) { text spell }.cast

      expect(effect).to eql 'Abracadabra!'
    end
  end
end
