require_relative '../helper'

describe Merlin::Spellbooks::HtmlSpellbook do

  context 'when create tags' do
    it 'returns object' do
      spell = Merlin::HtmlSpell.new { a.hide }

      expect(spell.cast).to eql "<a class='hide'></a>"
    end
  end

  describe '.doctype!' do
    it 'renders doctype' do
      spell = Merlin::HtmlSpell.new { doctype! }

      expect(spell.cast).to eql '<!DOCTYPE html>'
    end
  end
end
