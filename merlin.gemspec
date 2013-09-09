Gem::Specification.new do |spec|
  spec.required_ruby_version = '> 2.0.0'

  spec.name          = 'merlin'
  spec.version       = '0.0.1'
  spec.summary       = 'An HTML templating engine which uses Ruby syntax.'
  spec.description   = 'With Merlin you may generate HTML using plain Ruby.'

  spec.add_development_dependency 'rspec',      '>= 2.11.0'

  spec.add_development_dependency 'rails',        '>= 3.2.13'
  spec.add_development_dependency 'actionpack',   '>= 3.2.13'
  spec.add_development_dependency 'activemodel',  '>= 3.2.13'

  spec.files         = Dir['{lib,test,bin}/**/*', '[A-Z]*']
  spec.executables   = spec.files.grep(%r{^bin/}) { |f| File.basename(f) }
  spec.test_files    = spec.files.grep(%r{^(test|spec|features)/})

  spec.author        = 'Krugloff'
  spec.email         = 'mr.krugloff@gmail.com'
  spec.license       = 'MIT'
end
