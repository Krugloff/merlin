require_relative '../helper'

describe Merlin::Builders::HtmlSpellBuilder do
  SpellBuilder = Merlin::Builders::HtmlSpellBuilder

  context 'when render content' do
    it 'does not save tags' do
      ( builder = SpellBuilder.new ).content_for { `Abracadabra!` }

      expect(builder._tags).to be_empty
    end

    it 'escapes text' do
      effect = SpellBuilder.new.content_for('<span>Abracadabra!</span>')

      expect(effect.first.to_str)
        .to eql '&lt;span&gt;Abracadabra!&lt;/span&gt;'
    end

    it 'does not escape block' do
      effect = SpellBuilder.new.content_for { span 'Abracadabra!' }

      expect(effect.first.to_str).to eql '<span>Abracadabra!</span>'
    end
  end

  describe '.text' do
    it 'escapes text' do
      spell = Merlin::HtmlSpell.new { text '<span>Hello World!</span>' }

      expect(spell.cast).to eql '&lt;span&gt;Hello World!&lt;/span&gt;'
    end
  end

  describe '.`' do
    it 'escapes text' do
      spell = Merlin::HtmlSpell.new { `<span>Hello World!</span>` }

      expect(spell.cast).to eql '&lt;span&gt;Hello World!&lt;/span&gt;'
    end
  end

  describe '.text!' do
    it 'does not escape text' do
      spell = Merlin::HtmlSpell.new { text! '<span>Hello World!</span>' }

      expect(spell.cast).to eql '<span>Hello World!</span>'
    end
  end
end
