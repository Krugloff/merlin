# Merlin

With Merlin you may generate HTML using plain Ruby. Based on Mab, which based on Markaby.

## Installation

Add this line to your application's Gemfile:

`gem 'merlin', git: 'http://github.com/Krugloff/cando'`

And then execute:

`$ bundle`

Or install it yourself as:

`$ gem install merlin --source 'http://github.com/Krugloff/cando'`

## Usage

### Генерирование HTML

~~~~~ ruby
  require 'merlin'
  spell = Merlin::HtmlSpell.new do
    doctype!
    html do
      head do
        link rel: 'stylesheet', href: 'style.css'
        script src: 'jquery.js'
      end

      body :id => :frontpage do
        h1 'Hello World', :class => :main
      end
    end
  end

  spell.cast
~~~~~

В итоге будет получена HTML разметка:

~~~~~
  <!DOCTYPE html>
  <html>
    <head>
      <link rel='stylesheet' href='style.css'>
      <script src='jquery.js'></script>
    </head>

    <body id='frontpage'>
      <h1 class='main'>Hello World</h1>
    </body>
  </html>
~~~~~

Текстовые шаблоны тоже обрабатываются (приведет к тому же результату, что и выше):

~~~~~ ruby
  require 'merlin'
  spell = Merlin::HtmlSpell.new <<-SPELL
    doctype!
    html do
      head do
        link rel: 'stylesheet', href: 'style.css'
        script src: 'jquery.js'
      end

      body :id => :frontpage do
        h1 'Hello World', :class => :main
      end
    end
  SPELL

  spell.cast
~~~~~

### Обычный текст

~~~~~ ruby
  # Текст экранируется.
  Merlin::HtmlSpell.new { text '<span>Hello World!</span>' }.cast
  Merlin::HtmlSpell.new { `<span>Hello World!</span>` }.cast

  # -> '&lt;span&gt;Hello World!&lt;/span&gt;'

  # За что я люблю Ruby:
  Merlin::HtmlSpell.new do
    <<-`TEXT`
      Big Text. Very Big Text.
      Multiline.
      And Big.
      Very Big Text.
    TEXT
  end.cast

  # Текст не экранируется.
  Merlin::HtmlSpell.new { text! '<span>Hello World!</span>' }.cast
  # -> '<span>Hello World!</span>'
~~~~~

### Теги

~~~~~ ruby
  # Обычные:
  Merlin::HtmlSpell.new { a }.cast  # -> '<a></a>'

  # Одиночные:
  Merlin::HtmlSpell.new { hr }.cast # -> '<hr>'
~~~~~

#### Содержимое тега

~~~~~ ruby
  # Текст экранируется, но не обрабатывается.
  Merlin::HtmlSpell.new { a '<span>Hello World!</span>' }.cast
  # -> '<a>&lt;span&gt;Hello World!&lt;/span&gt;</a>'

  # А содержимое блока обрабатывается, но не экранируется. Будьте осторожны.
  Merlin::HtmlSpell.new { a { span 'Hello World!' } }.cast
  # -> '<a><span>Hello World!</span></a>'
~~~~~

#### Свойства тега

~~~~~ ruby
  Merlin::HtmlSpell.new { a href: ?# }.cast
  # -> "<a href='#'></a>"
~~~~~

#### Классы и идентификаторы

Классы:

~~~~~ ruby
  Merlin::HtmlSpell.new { a class: 'hide' }.cast
  Merlin::HtmlSpell.new { a.klass 'hide' }.cast
  Merlin::HtmlSpell.new { a.hide }.cast

  # -> "<a class='hide'></a>"
~~~~~

Идентификаторы:

~~~~~ ruby
  Merlin::HtmlSpell.new { a id: 'hide' }.cast
  Merlin::HtmlSpell.new { a.id 'hide' }.cast
  Merlin::HtmlSpell.new { a.hide! }.cast

  # -> "<a id='hide'></a>"
~~~~~

Можно добавлять несколько класов или идентификаторов:

~~~~~ ruby
  Merlin::HtmlSpell.new do
    a(class: 'hide', id: 'comments')
      .id('main_thread').klass('secure')
      .main!.black
  end.cast
  # -> "<a class='hide secure black' id='comments main_thread main'></a>"
~~~~~

Можно изменять свойства:

~~~~~ ruby
  Merlin::HtmlSpell.new { a(href: ?#).hide(href: 'www.example.com') }.cast
  # -> "<a href='www.example.com' class='hide'></a>"
~~~~~

Или добавлять содержимое:

~~~~~ ruby
  Merlin::HtmlSpell.new do
    a.hide { i.icon.icon_white }
  end.cast

  # -> "<a class='hide'><i class='icon icon_white'></i></a>"

  Merlin::HtmlSpell.new { a.hide 'Abracadbra!' }.cast
  # -> "<a class='hide'>Abracadbra!</a>"
~~~~~

### Использование объектов

Для заклинаний могут потребоваться различные артефакты :)

~~~~~ ruby
  Merlin::HtmlSpell.new(title: 'Abracadabra!') { text @title }.cast
  # -> 'Abracadabra!'

  ( artefact = Object.new ).instance_variable_set :@title, 'Abracadabra!'
  Merlin::HtmlSpell.new(artefact) { text @title }.cast
  # -> 'Abracadabra!'

  ( artefact = Object.new ).define_singleton_method(:spell) { 'Abracadabra!' }
  Merlin::HtmlSpell.new(artefact) { text spell }.cast
  # -> 'Abracadabra!'
~~~~~

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request
