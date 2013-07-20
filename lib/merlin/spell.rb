module Merlin
  class Spell
    def initialize(context_or_template = nil, **assigns, &template)
      @context = context_or_template unless context_or_template.is_a? String
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

      def _render_template
        case @template
        when String
          @builder.instance_eval @template, __FILE__, __LINE__
        when Proc
          @builder.instance_exec &@template
        end
        @builder.to_str
      end
  end
end

# В зависимости от настроек должен загружаться тот или иной Builder (с использованием необходимого модуля).

# Merlin.spells = HtmlSpell
# ActV....regis :spell, HtmlSpell.new ?

# bin/ spellcast [-spell=HtmlSpell (-r)equire] <file> || text
