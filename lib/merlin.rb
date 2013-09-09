module Merlin
  autoload :Spell,     'merlin/spell'
  autoload :HtmlSpell, 'merlin/html_spell'

  module Builders
    autoload :SpellBuilder,     'merlin/builders/spell_builder'
    autoload :HtmlSpellBuilder, 'merlin/builders/html_spell_builder'
  end

  module Spellbooks
    autoload :BaseSpellbook, 'merlin/spellbooks/base_spellbook'
    autoload :HtmlSpellbook, 'merlin/spellbooks/html_spellbook'
    autoload :RailsSpellbook, 'merlin/spellbooks/rails_spellbook'
  end
end

if defined? Rails and defined? ActionView::Template
  Merlin::Builders::HtmlSpellBuilder
    .send :include, Merlin::Spellbooks::RailsSpellbook

  ActionView::Template.register_template_handler :spell, Merlin::HtmlSpell
end

