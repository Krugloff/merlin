class HtmlSpellBuilderTest < Test::Unit::TestCase
  SpellBuilder = Merlin::Builders::HtmlSpellBuilder

  test 'should not save tags when render content' do
    ( builder = SpellBuilder.new ).content_for { `Abracadabra!` }

    assert_empty builder._tags
  end

  ##### Plain Text
  test 'should render plain text' do
    spell = Merlin::HtmlSpell.new { text 'Hello World!' }

    assert_equal 'Hello World!', spell.cast
  end

  test 'should render plain text with magic' do
    spell = Merlin::HtmlSpell.new { `Hello World!` }

    assert_equal 'Hello World!', spell.cast
  end

  ##### Escaping
  test 'should escape plain text' do
    spell = Merlin::HtmlSpell.new { `<span>Hello World!</span>` }

    assert_equal '&lt;span&gt;Hello World!&lt;/span&gt;', spell.cast
  end

  test 'should not escape plain text when mark' do
    spell = Merlin::HtmlSpell.new { text! '<span>Hello World!</span>' }

    assert_equal '<span>Hello World!</span>', spell.cast
  end

  test 'should escape text content' do
    effect = SpellBuilder.new.content_for('<span>Abracadabra!</span>')

    assert_equal '&lt;span&gt;Abracadabra!&lt;/span&gt;', effect.first.to_str
  end

  test 'should not escape block content' do
    effect = SpellBuilder.new.content_for { span 'Abracadabra!' }

    assert_equal '<span>Abracadabra!</span>', effect.first.to_str
  end
end
