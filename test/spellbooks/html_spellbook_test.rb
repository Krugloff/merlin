require 'merlin'

class HtmlSpellbookTest < Test::Unit::TestCase
  # Этот тест проверяет значение, возвращаемое при создании тега.
  test 'should return tag object' do
    spell = Merlin::HtmlSpell.new { a.hide }

    assert_equal "<a class='hide'></a>", spell.cast
  end

  ##### Normal tags
  test 'should render normal tags' do
    spell = Merlin::HtmlSpell.new { a 'Hello World!' }

    assert_equal '<a>Hello World!</a>', spell.cast
  end

  test 'should render normal tags with block' do
    spell = Merlin::HtmlSpell.new { a { `Hello World!` } }

    assert_equal '<a>Hello World!</a>', spell.cast
  end

  test 'should render normal tags with nested tag as block content' do
    spell = Merlin::HtmlSpell.new { a { i 'Hello World!' } }

    assert_equal '<a><i>Hello World!</i></a>', spell.cast
  end

  ##### Void tags
  test 'should render void tags' do
    spell = Merlin::HtmlSpell.new { hr }

    assert_equal '<hr>', spell.cast
  end

  ###### Attributes
  test 'should render normal tags with attribute' do
    spell = Merlin::HtmlSpell.new { a 'Hello World!', href: ?# }

    assert_equal "<a href='#'>Hello World!</a>", spell.cast
  end

  test 'should render normal tags with attribute (symbol value)' do
    spell = Merlin::HtmlSpell.new { a 'Hello World!', href: :example }

    assert_equal "<a href='example'>Hello World!</a>", spell.cast
  end

  test 'should render normal tags with attribute and block' do
    spell = Merlin::HtmlSpell.new { a(href: ?#) { `Hello World!` } }

    assert_equal "<a href='#'>Hello World!</a>", spell.cast
  end

  test 'should render normal tags with some attributes' do
    spell = Merlin::HtmlSpell.new do
      a 'Hello World!', href: ?#, title: 'Hello!'
    end

    assert_equal "<a href='#' title='Hello!'>Hello World!</a>", spell.cast
  end

  test 'should render void tags with attribute' do
    spell = Merlin::HtmlSpell.new { hr width: '3px' }

    assert_equal "<hr width='3px'>", spell.cast
  end

  test 'should render void tags with some attributes' do
    spell = Merlin::HtmlSpell.new { hr width: '3px', height: '4px' }

    assert_equal "<hr width='3px' height='4px'>", spell.cast
  end

  ###### Tags
  VOID_TAG   = Merlin::Spellbooks::HtmlSpellbook::VoidTag
  NORMAL_TAG = Merlin::Spellbooks::HtmlSpellbook::NormalTag

  test 'should add class to tag' do
    tag = VOID_TAG.new :i

    assert_equal "<i class='hide'>", tag.hide.to_str
  end

  test 'should add class to tag when helper' do
    tag = VOID_TAG.new :i

    assert_equal "<i class='hide'>", tag.klass('hide').to_str
  end

  test 'should add some class to tag' do
    tag = VOID_TAG.new :i

    assert_equal "<i class='hide secure'>", tag.hide.secure.to_str
  end

  test 'should add some class to tag when atributes' do
    tag = VOID_TAG.new :i

    assert_equal "<i class='hide secure'>", tag.hide(class: 'secure').to_str
  end

  test 'should add id to tag' do
    tag = VOID_TAG.new :i

    assert_equal "<i id='comments'>", tag.comments!.to_str
  end

  test 'should add id to tag when helper' do
    tag = VOID_TAG.new :i

    assert_equal "<i id='comments'>", tag.id('comments').to_str
  end

  test 'should add id and class to tag' do
    tag = VOID_TAG.new :i

    assert_equal "<i class='hide' id='comments'>", tag.hide.comments!.to_str
  end

  test 'should add id and class to tag when attributes' do
    tag = VOID_TAG.new :i

    assert_equal "<i class='hide' id='comments'>",
      tag.hide(id: 'comments').to_str
  end

  SpellBuilder = Merlin::Builders::HtmlSpellBuilder

  test 'should render block content' do
    tag = NORMAL_TAG.new(SpellBuilder.new, :a)

    assert_equal "<a class='hide'><i>Hello World!</i></a>",
      tag.hide { i 'Hello World!' }.to_str, tag.content
  end

  test 'should render text content' do
    tag = NORMAL_TAG.new(SpellBuilder.new, :a)

    assert_equal "<a class='hide'>Hello World!</a>",
      tag.hide('Hello World!').to_str, tag.content
  end

  ##### Helpers
  test 'should render doctype' do
    spell = Merlin::HtmlSpell.new { doctype! }

    assert_equal '<!DOCTYPE html>', spell.cast
  end
end
