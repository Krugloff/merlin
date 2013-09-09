module Merlin module Spellbooks module HtmlSpellbook
  NORMAL_TAGS =
    %i[a abbr acronym address applet article aside audio b basefont bdi bdo big blockquote body button canvas caption center cite code colgroup datalist dd del details dfn dir div dl dt em fieldset figcaption figure font footer form frame frameset h1 h2 h3 h4 h5 h6 head header hgroup html i iframe ins kbd label legend li link map mark math menu meter nav noframes noscript object ol optgroup option output p pre progress q rp rt ruby s samp script section select small span strike strong style sub summary sup svg table tbody td textarea tfoot th thead time title tr tt u ul var video xmp]

  VOID_TAGS =
    %i[base link meta hr br wbr img embed param source track area col input keygen command]

  NORMAL_TAGS.each do |tag|
    define_method tag do |content = nil, **attributes, &template|
      content = tags_for content, &template
      # Hack for return tag.
      _tags[_tags.size] = NormalTag.new(self, tag, attributes, content)
    end
  end

  VOID_TAGS.each do |tag|
    define_method tag do | attributes = {} |
      # Hack for return tag.
      _tags[_tags.size] = VoidTag.new(tag, attributes)
    end
  end

  def doctype!
    text! '<!DOCTYPE html>'
  end

  class Tag
    def to_str; end

    def klass(name)
      @attributes[:class] += " #{name}"
      self
    end

    def id(name)
      @attributes[:id] += " #{name}"
      self
    end

    # Add class or id.
    def method_missing(class_or_id, content = nil, **attributes, &template)
      class_or_id = class_or_id.to_s
      self.send class_or_id.end_with?(?!) ? :id : :klass,
        class_or_id.chomp(?!)

      _merge attributes

      @content.concat @builder.tags_for(content, &template) \
        if @builder

      self
    end

    private
      # Проверить перевод для открывающего тега.
      def _open_tag(name, attributes)
        '<' + [ name, _prepare_attributes(attributes) ].join(' ').strip + '>'
      end

      def _prepare_attributes(attributes)
        attributes.map { |key, value| "#{key}='#{value.strip}'" }.join ' '
      end

      def _merge(attributes = {})
        @attributes ||= Hash.new('')

        attributes.each do |key, value|
          value = value.to_s
          case key = key.to_sym
          when :class
            self.klass value
          when :id
            self.id value
          else
            @attributes[key] = value
          end
        end
      end
  end

  class NormalTag < Tag
    attr_accessor :builder, :name, :attributes, :content

    def initialize(builder, tag, attributes = {}, content = [])
      @builder = builder
      @name = tag.to_s
      @content = content
      _merge attributes
    end

    def to_str
      opening = _open_tag @name, @attributes
      closing = "</#{@name}>"
      content = @builder.to_str @content

      _pretty_html opening, content, closing
    end

    private
      def _pretty_html(opening, content = '', closing)
        need_pretty = @name.index( /(html|body|head)/ ) ||
          @content.size > 1 ||
          content.length > 60 ||
          content.index( /\n/ )
        pretty = need_pretty ? "\n" : ''

        # Indent using two spaces.
        content = content
          .split("\n")
          .map { |string| string.insert 0, '  '  }
          .join("\n") if need_pretty

        html = [ opening, content, closing ].join pretty

        need_pretty ? html.concat("\n") : html
      end
  end

  class VoidTag < Tag
    attr_accessor :name, :attributes

    def initialize(tag, attributes = {})
      @name = tag
      _merge attributes
    end

    def to_str
      _open_tag @name, @attributes
    end
  end
end end end
