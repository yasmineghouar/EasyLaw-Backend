# EasyLaw-Backend

1) Créer une base de données nommée easyLawDb dans PostgreSQL avec l'utilisateur 'postgres' et un mot de passe vide. 

2) flask shell ===>  pour lancer un shell interactif Flask avec l'application chargée

3) db.create_all() ===> pour créer toutes les tables définies dans nos modèles de base de données SQLAlchemy
4) Pour l'insertion des données initiales, exécuter les scripts suivants :
 
 ===> python insertionDomains.py
 ===> python insertionBDD_mahkama.py
 ===> python insertionBDD_majliss_test.py
 ===> python insertionLaws.py
 ===> python insertionPlanTarification.py
 ===> python insertionFactures.py  (Cela permet de créer un administrateur avec l'email abbaci@esi.dz et le mot de passe 123.)

5) flask run --port 8000 ===> démarrer l'application Flask sur le port 8000

# chatbot requirements : 
cohere
pinecone-client
configparser
langchain-community

===> pip install cohere pinecone-client configparser langchain-community
