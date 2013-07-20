require 'merlin'

class SpellTest < Test::Unit::TestCase
  # Casting
  test 'should cast text template' do
    effect = Merlin::Spell.new("`Abracadabra!`").cast

    assert_equal "Abracadabra!\n", effect
  end

  test 'should cast block template' do
    spell = Merlin::Spell.new { `Abracadabra!` }
    effect = spell.cast

    assert_equal "Abracadabra!\n", effect
  end

  ##### Artefacts
  test 'should init vars from args' do
    spell = Merlin::Spell.new(title: 'Abracadabra!') { text @title }
    effect = spell.cast

    assert_equal "Abracadabra!\n", effect
  end

  test 'should init vars from context object' do
    ( context = Object.new ).instance_variable_set :@title, 'Abracadabra!'
    spell = Merlin::Spell.new(context) { text @title }
    effect = spell.cast

    assert_equal "Abracadabra!\n", effect
  end

  test 'should send missing method to context' do
    ( context = Object.new ).define_singleton_method(:title) { 'Abracadabra!' }
    effect = Merlin::Spell.new(context) { text title }.cast

    assert_equal "Abracadabra!\n", effect
  end
end
