require_relative 'helper'

describe Merlin::Spell do

  context 'when template' do
    it 'renders text' do
      effect = Merlin::Spell.new("`Abracadabra!`").cast

      expect(effect).to eql "Abracadabra!\n"
    end

    it 'renders block' do
      spell = Merlin::Spell.new { `Abracadabra!` }
      effect = spell.cast

      expect(effect).to eql "Abracadabra!\n"
    end
  end

  context 'when vars' do
    it 'inits vars' do
      spell = Merlin::Spell.new(title: 'Abracadabra!') { text @title }
      effect = spell.cast

      expect(effect).to eql "Abracadabra!\n"
    end
  end

  context 'when context object' do
    it 'inits vars' do
      ( context = Object.new ).instance_variable_set :@title, 'Abracadabra!'
      spell = Merlin::Spell.new(context) { text @title }
      effect = spell.cast

      expect(effect).to eql "Abracadabra!\n"
    end

    it 'sends missing method to context' do
      ( context = Object.new ).define_singleton_method(:title) { 'Abracadabra!' }
      effect = Merlin::Spell.new(context) { text title }.cast

      expect(effect).to eql "Abracadabra!\n"
    end
  end
end
