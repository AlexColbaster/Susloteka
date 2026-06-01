from django.db import migrations


DIRECTORS = [
    ('Christopher Nolan', 'Британско-американский режиссёр, известный нелинейным монтажом и масштабными блокбастерами.', 'https://en.wikipedia.org/wiki/Christopher_Nolan'),
    ('Quentin Tarantino', 'Американский режиссёр, сценарист и продюсер, прославившийся стильными диалогами и жанровыми миксами.', 'https://en.wikipedia.org/wiki/Quentin_Tarantino'),
    ('Steven Spielberg', 'Американский режиссёр и продюсер, один из самых влиятельных авторов голливудского кино.', 'https://en.wikipedia.org/wiki/Steven_Spielberg'),
    ('Martin Scorsese', 'Американский режиссёр, известный криминальными драмами и вниманием к моральному выбору героев.', 'https://en.wikipedia.org/wiki/Martin_Scorsese'),
    ('Ridley Scott', 'Британский режиссёр, работающий в историческом, научно-фантастическом и военном кино.', 'https://en.wikipedia.org/wiki/Ridley_Scott'),
    ('James Cameron', 'Канадский режиссёр, сочетающий технические инновации с крупными зрелищными проектами.', 'https://en.wikipedia.org/wiki/James_Cameron'),
    ('David Fincher', 'Американский режиссёр, известный холодной визуальной эстетикой и психологическими триллерами.', 'https://en.wikipedia.org/wiki/David_Fincher'),
    ('Denis Villeneuve', 'Канадский режиссёр, снимающий атмосферные драмы и крупную научную фантастику.', 'https://en.wikipedia.org/wiki/Denis_Villeneuve'),
    ('Wes Anderson', 'Американский режиссёр с узнаваемой симметричной композицией и ироничным тоном.', 'https://en.wikipedia.org/wiki/Wes_Anderson'),
    ('Sofia Coppola', 'Американская режиссёрка, работающая с темами одиночества, идентичности и внутренней тишины.', 'https://en.wikipedia.org/wiki/Sofia_Coppola'),
    ('Greta Gerwig', 'Американская режиссёрка и сценаристка, снимающая современные истории взросления.', 'https://en.wikipedia.org/wiki/Greta_Gerwig'),
    ('Bong Joon-ho', 'Южнокорейский режиссёр, мастер социального жанрового кино с острой сатирой.', 'https://en.wikipedia.org/wiki/Bong_Joon-ho'),
    ('Park Chan-wook', 'Южнокорейский режиссёр, известный стильными триллерами и мрачной эстетикой.', 'https://en.wikipedia.org/wiki/Park_Chan-wook'),
    ('Hayao Miyazaki', 'Японский аниматор и режиссёр, создатель поэтичных и человечных анимационных миров.', 'https://en.wikipedia.org/wiki/Hayao_Miyazaki'),
    ('Akira Kurosawa', 'Японский режиссёр, оказавший огромное влияние на мировое кино.', 'https://en.wikipedia.org/wiki/Akira_Kurosawa'),
    ('Takashi Miike', 'Японский режиссёр, работающий в широком спектре жанров от драмы до хоррора.', 'https://en.wikipedia.org/wiki/Takashi_Miike'),
    ('Alfonso Cuarón', 'Мексиканский режиссёр, известный визуально сложными и эмоциональными фильмами.', 'https://en.wikipedia.org/wiki/Alfonso_Cuarón'),
    ('Guillermo del Toro', 'Мексиканский режиссёр и сценарист, соединяющий фэнтези, хоррор и гуманизм.', 'https://en.wikipedia.org/wiki/Guillermo_del_Toro'),
    ('Pedro Almodóvar', 'Испанский режиссёр, работающий с яркой мелодрамой и сильными женскими образами.', 'https://en.wikipedia.org/wiki/Pedro_Almod%C3%B3var'),
    ('Lars von Trier', 'Датский режиссёр, известный провокационным авторским кино и экспериментами.', 'https://en.wikipedia.org/wiki/Lars_von_Trier'),
    ('Nuri Bilge Ceylan', 'Турецкий режиссёр, снимающий философские и созерцательные драмы.', 'https://en.wikipedia.org/wiki/Nuri_Bilge_Ceylan'),
    ('Paolo Sorrentino', 'Итальянский режиссёр, создающий визуально роскошные ироничные драмы.', 'https://en.wikipedia.org/wiki/Paolo_Sorrentino'),
    ('Federico Fellini', 'Итальянский режиссёр, автор сюрреалистичных и автобиографичных фильмов.', 'https://en.wikipedia.org/wiki/Federico_Fellini'),
    ('Bernardo Bertolucci', 'Итальянский режиссёр, известный масштабными историческими и психологическими драмами.', 'https://en.wikipedia.org/wiki/Bernardo_Bertolucci'),
    ('Ingmar Bergman', 'Шведский режиссёр, исследующий веру, смерть и человеческие отношения.', 'https://en.wikipedia.org/wiki/Ingmar_Bergman'),
    ('Agnieszka Holland', 'Польская режиссёрка, работающая в кино и на телевидении с социальными темами.', 'https://en.wikipedia.org/wiki/Agnieszka_Holland'),
    ('Andrei Tarkovsky', 'Советский режиссёр, известный медитативным и философским киноязыком.', 'https://en.wikipedia.org/wiki/Andrei_Tarkovsky'),
    ('Sergei Eisenstein', 'Советский режиссёр, один из основоположников монтажной теории в кино.', 'https://en.wikipedia.org/wiki/Sergei_Eisenstein'),
    ('Elem Klimov', 'Советский режиссёр, снимающий мощные и трагические фильмы о войне и человеке.', 'https://en.wikipedia.org/wiki/Elem_Klimov'),
    ('Kira Muratova', 'Советская и украинская режиссёрка, известная нестандартным авторским стилем.', 'https://en.wikipedia.org/wiki/Kira_Muratova'),
    ('Eldar Ryazanov', 'Советский режиссёр, мастер народных комедий и сатирических мелодрам.', 'https://en.wikipedia.org/wiki/Eldar_Ryazanov'),
    ('Nikita Mikhalkov', 'Российский режиссёр, актёр и продюсер, работающий с историческими и драматическими сюжетами.', 'https://en.wikipedia.org/wiki/Nikita_Mikhalkov'),
    ('Fyodor Bondarchuk', 'Российский режиссёр, актёр и продюсер, работающий в жанровом и коммерческом кино.', 'https://en.wikipedia.org/wiki/Fyodor_Bondarchuk'),
    ('Zhang Yimou', 'Китайский режиссёр, известный визуальной выразительностью и историческими драмами.', 'https://en.wikipedia.org/wiki/Zhang_Yimou'),
    ('Wong Kar-wai', 'Гонконгский режиссёр, создающий меланхоличные истории о любви и времени.', 'https://en.wikipedia.org/wiki/Wong_Kar-wai'),
    ('John Woo', 'Гонконгский режиссёр, прославившийся стильными боевиками и хореографией перестрелок.', 'https://en.wikipedia.org/wiki/John_Woo'),
    ('Ang Lee', 'Тайваньско-американский режиссёр, работающий в разных жанрах и культурных контекстах.', 'https://en.wikipedia.org/wiki/Ang_Lee'),
    ('Asghar Farhadi', 'Иранский режиссёр, известный тонкими социальными драмами и моральными дилеммами.', 'https://en.wikipedia.org/wiki/Asghar_Farhadi'),
    ('Jafar Panahi', 'Иранский режиссёр, снимающий социально острое кино с документальной энергией.', 'https://en.wikipedia.org/wiki/Jafar_Panahi'),
    ('Aamir Khan', 'Индийский актёр и режиссёр, участвующий в создании социально ориентированного кино.', 'https://en.wikipedia.org/wiki/Aamir_Khan'),
    ('Satyajit Ray', 'Индийский режиссёр, классик гуманистического авторского кино.', 'https://en.wikipedia.org/wiki/Satyajit_Ray'),
    ('Kabir Khan', 'Индийский режиссёр, работающий с коммерческим кино и историческими сюжетами.', 'https://en.wikipedia.org/wiki/Kabir_Khan'),
    ('Anurag Kashyap', 'Индийский режиссёр, известный жёстким реализмом и криминальными историями.', 'https://en.wikipedia.org/wiki/Anurag_Kashyap'),
    ('Taika Waititi', 'Новозеландский режиссёр, сочетающий юмор, жанр и эмоциональную теплоту.', 'https://en.wikipedia.org/wiki/Taika_Waititi'),
    ('George Miller', 'Австралийский режиссёр, создатель динамичных и визуально мощных экшен-фильмов.', 'https://en.wikipedia.org/wiki/George_Miller_(filmmaker)'),
    ('Peter Jackson', 'Новозеландский режиссёр, известный эпическими фэнтези-экранизациями.', 'https://en.wikipedia.org/wiki/Peter_Jackson'),
    ('Michael Haneke', 'Австрийский режиссёр, работающий с психологической напряжённостью и социальным дискомфортом.', 'https://en.wikipedia.org/wiki/Michael_Haneke'),
    ('Yorgos Lanthimos', 'Греческий режиссёр, известный абсурдистскими и странными авторскими фильмами.', 'https://en.wikipedia.org/wiki/Yorgos_Lanthimos'),
    ('François Ozon', 'Французский режиссёр, работающий с драмой, триллером и иронией.', 'https://en.wikipedia.org/wiki/Fran%C3%A7ois_Ozon'),
    ('Luc Besson', 'Французский режиссёр и продюсер, известный динамичным жанровым кино.', 'https://en.wikipedia.org/wiki/Luc_Besson'),
    ('Claude Lelouch', 'Французский режиссёр, снимающий романтические и жизненные истории.', 'https://en.wikipedia.org/wiki/Claude_Lelouch'),
    ('Robert Bresson', 'Французский режиссёр, знаменитый аскетичным и духовным стилем.', 'https://en.wikipedia.org/wiki/Robert_Bresson'),
]


def seed_directors(apps, schema_editor):
    Director = apps.get_model('films', 'Director')
    for name, description, link in DIRECTORS:
        Director.objects.get_or_create(
            name=name,
            defaults={
                'description': description,
                'link': link,
            },
        )


def unseed_directors(apps, schema_editor):
    Director = apps.get_model('films', 'Director')
    Director.objects.filter(name__in=[name for name, _, _ in DIRECTORS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0005_director_link'),
    ]

    operations = [
        migrations.RunPython(seed_directors, unseed_directors),
    ]
