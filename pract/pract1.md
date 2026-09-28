# Задание 3
```bash
#!/bin/bash
if [ "$#" -eq 0 ]; then
    echo "Использование: $0 <текст>" >&2
    exit 1
fi
text="$1"
length=${#text}
line="+"
for ((i = 0; i < length + 2; i++)); do
    line+="-"
done
line+="+"
printf '%s\n' "$line"
printf '| %s |\n' "$text"
printf '%s\n' "$line"
```

# Задание 4
```bash
#!/bin/bash
if [ "$#" -eq 0 ]; then
    echo "Использование: $0 <файл>" >&2
    exit 1
fi
grep -oE '[A-Za-z_][A-Za-z0-9_]*' "$1" | sort -u | paste -sd ' ' -
```

# Задание 5
```bash
#!/bin/bash
if [ "$#" -ne 1 ]; then
        echo "Использование: $0 <файл>" >&2
        exit 1
fi
if [ ! -f "$1" ]; then
        echo "Ошибка: файл '$1' не найден" >&2
        exit 1
fi
sudo chmod 755 "$1" || exit 1
sudo cp "$1" /usr/local/bin/ || exit 1
echo "Команда '$(basename "$1")' установлена в /usr/local/bin"
```
