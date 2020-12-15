# parsing-Rozeka
Скрипт для парсинга продуктов с сайта Розетки. 

-h, --help show this help message and exit

-s SEARCH, --search ищет слово или фразу и сохраняет найденные карточки (на rapberry pi ищет только на латинице)

-I, --image сохраняет изображение товара в папку images 

-a, --articule id продука 

-l, --link ссылка на продукт 

-t, --title название продукта 

-i, --imagelink ссылка на изображение продукта 

-r, --rating рейтинг продукта 

-R, --reviews колличество отзывов 

-p, --price цена на товар актуальная (если есть промо цена, то промоцена)

-o, --oldprice цена на товар, без промо 

-d, --description описание товара, если есть 

-f FILE, --file FILE имя файла с ссылками на категории которые необходим парсить, каждая ссылка с новой строки в виде https://rozetka.com.ua/skrapbuking-i-kardmejking/c4632201/ 

-w WRITE, --write WRITE сохранить результаты парсинга в файл, по умолчанию используюется файл rozetka.csv


Пример запуска скрипта

sudo python3 parser-rozetka.py -ltipI -f file.txt

откроет ссылку из file.txt - https://rozetka.com.ua/skrapbuking-i-kardmejking/c4632201/
сохратит в файл rozetka.csv название продукта, ссылку на продукт, ссылка на изображение товара, цену на товар и будет сохранять изображение товаров в папку images
