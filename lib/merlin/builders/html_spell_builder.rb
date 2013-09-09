require 'cgi'

module Merlin module Builders class HtmlSpellBuilder < SpellBuilder
  include Merlin::Spellbooks::HtmlSpellbook

  attr_accessor :_tags

  def initialize(*args)
    super
    @_tags = []
  end

  def to_str(tags = _tags)
    tags.map(&:to_str).join("\n")
  end

  def text(content)
    text! CGI.escapeHTML content if content
  end

  alias :` :text

  def text!(content)
    _tags << PlainText.new(content) if content
  end

  class PlainText
    def initialize(content)
      @content = content
    end

    def to_str
      @content
    end
  end

  # Save tags once.
  def content_for(content = nil, &template)
    begin
      current_tags = self._tags
      self._tags = []
      text content
      instance_exec &template if block_given?
      self._tags
    ensure
      self._tags = current_tags
    end
  end
end end end
