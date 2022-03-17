reticulate::virtualenv_create(envname = 'python3_env', python = '/usr/bin/python3')
reticulate::virtualenv_install(envname = 'python3_env', packages = c('pandas','numpy'), ignore_installed=TRUE)
reticulate::use_virtualenv('python3_env', required = T)
reticulate::source_python('generate_bracket.py')
output = main()
winner = output[[1]]
df = apply(output[[2]], 2, as.character)
df[df=='NaN'] = ""

