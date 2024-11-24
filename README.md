## Jaki model jest najlepszy dla naszego użytku?

Zakładam, że nie mamy mega kart graficznych, więc najlepszą opcją jest skorzystanie z jakiegoś API (choć możliwość lokalnego odpalenia pozostawiam). Dla modelu gpt4-o od OpenAI pogłębione testy nie stanowiły problemu. Inne modele gpt lub lżejsze (do 11 miliardów parametrów) dostępne na platformie ollama nie spełniają wymagań. 

## Jak zainstalować lokalnie wybrany model?

#### Potrzebujemy narzędzie!
$ curl -fsSL https://ollama.com/install.sh | sh

#### Teraz pora na instalację [wybranego](https://github.com/ollama/ollama?tab=readme-ov-file) modelu!

$ ollama pull <model_name>

wsm to tyle ;)


## Jak skorzystać z API OpenAI

No trzeba mieć kluczyk kurdelebele. Dodatkowo by użyć gpt4o trzeba wpłacić 5$.
