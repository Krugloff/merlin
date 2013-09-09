# Все внутренние переменные экземпляра лучше начинать с подчеркивания, чтобы они не переопределялись с переменными, переданными в шаблон.
module Merlin module Builders class SpellBuilder
  include Merlin::Spellbooks::BaseSpellbook

  def initialize(context = nil)
    @_context = context
    @_result  = ''
  end

  def to_str
    @_result
  end

  # Render plain text.
  def text(content)
    @_result << ( content + "\n" ) if content
  end

  alias :` :text

  # Delegate method to context object.
  def method_missing(name, *args, &block)
    super unless @_context.respond_to?(name, true)
    @_context.send name, *args, &block
  end
end end end
