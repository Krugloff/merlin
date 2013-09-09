# Prepend rails helpers.
module Merlin module Spellbooks module RailsSpellbook
  module Refinements
    # Нужен собственный FormBuilder.
    def capture(*args, &block)
      respond_to?(:merlin) ? merlin.capture(*args, &block) : super
    end
  end

  def capture(*args, &block)
    tags = self.tags_for nil, *args, &block
    self.to_str(tags).html_safe
  end

  ActionView::Base.send :prepend, Refinements

  #! label -> label_for
  class FormBuilder < ActionView::Helpers::FormBuilder
    def initialize(*args)
      super
      @template = @template.merlin
    end
  end

  TAG_HELPERS = %i[
    tag
    content_tag
    cdata_section
  ]

  URL_HELPERS = %i[
    link_to
    mail_to
    button_to
    link_to_if
    link_to_unless
    link_to_unless_current
  ]

  TEXT_HELPERS = %i[ simple_format ]

  RENDERING_HELPERS  = %i[ render ]

  RECORD_TAG_HELPERS = %i[
    div_for
    content_tag_for
  ]

  JAVASCRIPT_HELPER  = %i[
    javascript_tag
    javascript_cdata_section
    button_to_function
    link_to_function
  ]

  FORM_TAG_HELPERS   = %i[
    form_tag
    select_tag

    text_field_tag
    label_tag
    hidden_field_tag
    file_field_tag
    password_field_tag
    text_area_tag

    check_box_tag
    radio_button_tag

    submit_tag
    button_tag
    image_submit_tag

    field_set_tag

    color_field_tag
    search_field_tag
    telephone_field_tag
    phone_field_tag

    date_field_tag
    time_field_tag
    datetime_field_tag
    datetime_local_field_tag
    month_field_tag
    week_field_tag

    url_field_tag
    email_field_tag
    number_field_tag
    range_field_tag
    utf8_enforcer_tag
  ]

  FORM_OPTIONS_HELPERS = %i[
    collection_select
    grouped_collection_select
    time_zone_select
    collection_radio_buttons
    collection_check_boxes
  ]

  #! Instead select.
  def select_for(*args)
    text! select_for! *args
  end

  def select_for!(*args)
    @_context.select *args
  end
  #####

  FORM_HELPER = %i[
    text_field
    hidden_field
    file_field
    password_field
    text_area

    check_box
    radio_button

    submit
    button

    color_field
    search_field
    telephone_field
    phone_field

    date_field
    time_field
    datetime_field
    datetime_local_field
    month_field
    week_field

    url_field
    email_field
    number_field
    range_field
  ]

  # Я скопировал этот метод из Rails 4.0. И внес пару исправлений.
  # Почему-то без него содержимое формы пусто.
  # Если вы знаете как обойтись без этого, пожалуйста сообщите мне.
  def form_for(record, options = {}, &block)
    raise ArgumentError, "Missing block" unless block_given?
    html_options = options[:html] ||= {}
    options[:builder] = FormBuilder # Krugloff

    case record
    when String, Symbol
      object_name = record
      object      = nil
    else
      object      = record.is_a?(Array) ? record.last : record
      raise ArgumentError, "First argument in form cannot contain nil or be empty" unless object
      object_name = options[:as] || model_name_from_record_or_class(object).param_key
      apply_form_for_options!(record, object, options)
    end

    html_options[:data]   = options.delete(:data)   if options.has_key?(:data)
    html_options[:remote] = options.delete(:remote) if options.has_key?(:remote)
    html_options[:method] = options.delete(:method) if options.has_key?(:method)
    html_options[:authenticity_token] = options.delete(:authenticity_token)

    builder = instantiate_builder(object_name, object, options)
    output  = capture(builder, &block)

    html_options[:multipart] ||= builder.multipart?

    form_tag(options[:url] || {}, html_options) { concat output } # Krugloff.
  end

  def fields_for(record_name, record_object = nil, options = {}, &block)
    options[:builder] = FormBuilder
    text! @_context.fields_for record_name, record_object, options, &block
  end

  #! Instead label.
  def label_for(*args, &block)
    text! label_for! *args, &block
  end

  def label_for!(*args, &block)
    @_context.label *args, &block
  end
  #####

  DEBUG_HELPER = %i[ debug ]

  DATE_HELPERS = %i[
    date_select
    time_select
    datetime_select

    select_datetime
    select_date
    select_time
    select_second
    select_minute
    select_hour
    select_day
    select_month
    select_year

    time_tag
  ]

  CSRF_HELPERS = %i[
    csrf_meta_tags
    csrf_meta_tag
  ]

  #! `.provide` don't work.
  CAPTURE_HELPERS = %i[
    content_for
    provide
  ]

  ASSET_TAG_HELPERS = %i[
    javascript_include_tag
    stylesheet_link_tag
    auto_discovery_link_tag
    favicon_link_tag
    image_tag
    video_tag
    audio_tag
  ]

  HELPERS =
    TAG_HELPERS           +
    URL_HELPERS           +
    TEXT_HELPERS          +
    RENDERING_HELPERS     +
    RECORD_TAG_HELPERS    +
    JAVASCRIPT_HELPER     +
    FORM_TAG_HELPERS      +
    FORM_OPTIONS_HELPERS  +
    FORM_HELPER           +
    DEBUG_HELPER          +
    DATE_HELPERS          +
    CSRF_HELPERS          +
    CAPTURE_HELPERS       +
    ASSET_TAG_HELPERS

  # Отдельный метод для content_tag - в зависимисоти от того передан блок или нет.
  # Проверить field_set_tag
  HELPERS.each do |name|
    module_eval <<-METHOD , __FILE__, __LINE__ + 1
      def #{name}(*args, &block)
        html = @_context.#{name}(*args, &block)
        text! html if html
      end

      def #{name}!(*args, &block)
        @_context.#{name}(*args, &block)
      end
    METHOD
  end

  def concat(string); text! string; end
  def safe_concat(string); text string; end

  #? Render partial in current context.
  # def render(options = {}, locals = {}, &block)
  # end
end end end
