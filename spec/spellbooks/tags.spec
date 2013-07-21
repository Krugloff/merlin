require_relative '../helper'

describe 'Tags' do
  SpellBuilder = Merlin::Builders::HtmlSpellBuilder
  VOID_TAG     = Merlin::Spellbooks::HtmlSpellbook::VoidTag
  NORMAL_TAG   = Merlin::Spellbooks::HtmlSpellbook::NormalTag

  describe 'Normal Tags' do
    it 'renders' do
      spell = Merlin::HtmlSpell.new { a 'Hello World!' }

      expect(spell.cast).to eql '<a>Hello World!</a>'
    end

    context 'when content' do
      it 'renders text' do
        spell = Merlin::HtmlSpell.new { a 'Hello World!' }

        expect(spell.cast).to eql '<a>Hello World!</a>'
      end

      it 'renders block' do
        spell = Merlin::HtmlSpell.new { a { i 'Hello World!' } }

        expect(spell.cast).to eql '<a><i>Hello World!</i></a>'
      end
    end

    context 'when attributes' do
      it 'renders with attribute' do
        spell = Merlin::HtmlSpell.new { a 'Hello World!', href: ?# }

        expect(spell.cast).to eql "<a href='#'>Hello World!</a>"
      end

      it 'renders with attribute (symbol value)' do
        spell = Merlin::HtmlSpell.new { a 'Hello World!', href: :example }

        expect(spell.cast).to eql "<a href='example'>Hello World!</a>"
      end

      it 'renders with attributes' do
        spell = Merlin::HtmlSpell.new do
          a 'Hello World!', href: ?#, title: 'Hello!'
        end

        expect(spell.cast).to eql "<a href='#' title='Hello!'>Hello World!</a>"
      end

      it 'renders with content' do
        spell = Merlin::HtmlSpell.new { a(href: ?#) { `Hello World!` } }

        expect(spell.cast).to eql "<a href='#'>Hello World!</a>"
      end
    end
  end

  describe 'Void Tags' do
    it 'renders' do
      spell = Merlin::HtmlSpell.new { hr }

      expect(spell.cast).to eql '<hr>'
    end

    context 'when attributes' do
      it 'renders attribute' do
        spell = Merlin::HtmlSpell.new { hr width: '3px' }

        expect(spell.cast).to eql "<hr width='3px'>"
      end

      it 'renders attributes' do
        spell = Merlin::HtmlSpell.new { hr width: '3px', height: '4px' }

        expect(spell.cast).to eql "<hr width='3px' height='4px'>"
      end
    end
  end

  describe 'Helpers' do
    let(:tag) { VOID_TAG.new :i }
    let(:content_tag) { NORMAL_TAG.new(SpellBuilder.new, :a) }

    describe '.klass' do
      it 'renders class attribute' do
        html = tag.klass('hide').to_str

        expect(html).to eql "<i class='hide'>"
      end
    end

    describe '.id' do
      it 'renders id attribute' do
        html = tag.id('comments').to_str

        expect(html).to eql "<i id='comments'>"
      end
    end

    describe 'method missing' do
      context 'when no mark' do
        it 'renders class attribute' do
          html = tag.hide.to_str

          expect(html).to eql "<i class='hide'>"
        end

        it 'renders some class attribute' do
          html = tag.hide.secure.to_str

          expect(html).to eql "<i class='hide secure'>"
        end

        it 'renders attributes' do
          html = tag.hide(class: 'secure').to_str

          expect(html).to eql "<i class='hide secure'>"
        end

        it 'renders text content' do
          html = content_tag.hide('Hello World!').to_str

          expect(html).to eql "<a class='hide'>Hello World!</a>"
        end

        it 'renders block content' do
          html = content_tag.hide { i 'Hello World!' }.to_str

          expect(html).to eql "<a class='hide'><i>Hello World!</i></a>"
        end
      end

      context 'when mark' do
        it 'renders id attribute' do
          html = tag.comments!.to_str

          expect(html).to eql "<i id='comments'>"
        end
      end

      it 'returns tag object' do
        html = tag.hide.comments!.to_str

        expect(html).to eql "<i class='hide' id='comments'>"
      end
    end
  end
end
