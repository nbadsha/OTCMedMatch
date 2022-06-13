mkdir -p ~/.MedMatch/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.MedMatch/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.MedMatch/config.toml