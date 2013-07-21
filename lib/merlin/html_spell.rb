module Merlin class HtmlSpell < Spell
  def initialize(*args)
    super
    @builder = Builders::HtmlSpellBuilder.new @context
  end
end end
