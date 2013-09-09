module Merlin class Spell
  # For Rails.
  #? Add template.locals
  def self.call(template)
    <<-RENDER
    spell = #{self}.new( self, { } ) do
      #{template.source}
    end

    class << self
      attr_accessor :merlin
    end

    self.merlin = spell.builder

    spell.cast
    RENDER
  end

  attr_accessor :builder

  def initialize(context_or_template = nil, *args, **assigns, &template)
    @context = context_or_template unless context_or_template.is_a? String
    @args = args
    @assigns = assigns
    @template = template || context_or_template
    @builder = Builders::SpellBuilder.new @context
  end

  def cast
    _initialize_vars
    _render_template
  end

  private
    def _initialize_vars
      if @context
        @context.instance_variables.each do |var|
          @builder.instance_variable_set var,
            @context.instance_variable_get(var)
        end
      end

      @assigns.each do |key, value|
        @builder.instance_variable_set(:"@#{key}", value)
      end
    end

    #? Add test for args.
    def _render_template
      case @template
      when String
        @builder.instance_eval @template, __FILE__, __LINE__
      when Proc
        @builder.instance_exec *@args, &@template
      end
      @builder.to_str
    end
end end

# bin/ spellcast [-spell=HtmlSpell (-r)equire] <file> || text
