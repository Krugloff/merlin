require_relative '../helper'

describe Merlin::Builders::SpellBuilder do
  describe '.text' do
    it 'render text' do
      effect = Merlin::Spell.new { text 'Hello World!' }.cast

      expect(effect).to eql "Hello World!\n"
    end
  end

  describe '.`' do
    it 'render text' do
      effect = Merlin::Spell.new { `Hello World!` }.cast

      expect(effect).to eql "Hello World!\n"
    end
  end
end
