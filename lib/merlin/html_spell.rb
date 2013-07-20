require 'merlin'

module Merlin class HtmlSpell < Spell
  def initialize(context_or_template = nil, **assigns, &template)
    super
    @builder = Builders::HtmlSpellBuilder.new @context
  end
end end
