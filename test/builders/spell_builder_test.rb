require 'merlin'

class SpellBuilderTest < Test::Unit::TestCase
  SpellBuilder = Merlin::Builders::SpellBuilder

  test 'should render plain text' do
    effect = Merlin::Spell.new { text 'Hello World!' }.cast

    assert_equal "Hello World!\n", effect
  end

  test 'should render plain text with magic' do
    effect = Merlin::Spell.new { `Hello World!` }.cast

    assert_equal "Hello World!\n", effect
  end
end
