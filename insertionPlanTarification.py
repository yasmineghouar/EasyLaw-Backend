import psycopg2
from datetime import datetime

# Données à insérer dans la table tarification
donnees_a_inserer = [
    (3, 2, "Mensuelle", 2005, "البحث المتقدم عن الاجتهادات القضائية الخاصة بالمحكمة العليا ومجلس الدولة يُعَدُ خدمة حيوية للمحامين والباحثين في المجال القانوني، حيث يُمكّنهم من الوصول إلى قرارات واجتهادات القضاة في هذه المحاكم العليا. تُعتبر هذه القرارات والاجتهادات مرجعًا هامًا لفهم تطبيق القانون وتفسيره في مختلف المجالات القانونية.", True, datetime.strptime("2024-05-07 00:46:08.569128", "%Y-%m-%d %H:%M:%S.%f")),
    (4, 2, "Annuelle", 4900, "البحث المتقدم عن الاجتهادات القضائية الخاصة بالمحكمة العليا ومجلس الدولة يُعَدُ خدمة حيوية للمحامين والباحثين في المجال القانوني، حيث يُمكّنهم من الوصول إلى قرارات واجتهادات القضاة في هذه المحاكم العليا. تُعتبر هذه القرارات والاجتهادات مرجعًا هامًا لفهم تطبيق القانون وتفسيره في مختلف المجالات القانونية.", True, datetime.strptime("2024-05-07 00:46:16.545649", "%Y-%m-%d %H:%M:%S.%f")),
    (1, 1, "Annuelle", 4509, "البحث المتقدم عن القوانين الأساسي الجزائرية المنشورة في الجريدة الرسمية يعد أمرًا بالغ الأهمية للمهتمين بالقانون والقضايا القانونية في الجزائر", True, datetime.strptime("2024-05-07 00:44:48.778445", "%Y-%m-%d %H:%M:%S.%f")),
    (6, 3, "Mensuelle", 2000, "ربوت الذكي للإجابة عن الأسئلة المتعلقة بالقانون، يمثل ذلك خدمة مبتكرة ومفيدة تستخدم تقنيات الذكاء الاصطناعي لتقديم إجابات فورية ودقيقة على استفسارات المستخدمين في مختلف المواضيع القانونية. يمكن أن يشمل نطاق هذه الخدمة مجموعة واسعة من الأسئلة والاستفسارات، بما في ذلك استشارات قانونية عامة، وتفسير للتشريعات، وتوجيهات حول الإجراءات القانونية، وغيرها.", True, datetime.strptime("2024-05-07 00:46:38.333753", "%Y-%m-%d %H:%M:%S.%f")),
    (7, 4, "Mensuelle", 2000, "لإشعارات المتعلقة بمجالات الاهتمام، فتُعَدُ خدمة ضرورية للأفراد والمهتمين بمواكبة التطورات القانونية في مجالات معينة. من خلال تلقي الإشعارات، يمكن للمستخدمين البقاء على اطلاع دائم بآخر التحديثات والتغييرات في القوانين واللوائح ذات الصلة بمجالاتهم الخاصة، مما يساعدهم على اتخاذ القرارات الصائبة والمستنيرة والتفاعل مع التغييرات بشكل فعال.", True, datetime.strptime("2024-05-07 00:46:51.473999", "%Y-%m-%d %H:%M:%S.%f")),
    (8, 4, "Annuelle", 2000, "لإشعارات المتعلقة بمجالات الاهتمام، فتُعَدُ خدمة ضرورية للأفراد والمهتمين بمواكبة التطورات القانونية في مجالات معينة. من خلال تلقي الإشعارات، يمكن للمستخدمين البقاء على اطلاع دائم بآخر التحديثات والتغييرات في القوانين واللوائح ذات الصلة بمجالاتهم الخاصة، مما يساعدهم على اتخاذ القرارات الصائبة والمستنيرة والتفاعل مع التغييرات بشكل فعال.", True, datetime.strptime("2024-05-07 00:47:01.233487", "%Y-%m-%d %H:%M:%S.%f")),
    (5, 3, "Annuelle", 2500, "ربوت الذكي للإجابة عن الأسئلة المتعلقة بالقانون، يمثل ذلك خدمة مبتكرة ومفيدة تستخدم تقنيات الذكاء الاصطناعي لتقديم إجابات فورية ودقيقة على استفسارات المستخدمين في مختلف المواضيع القانونية. يمكن أن يشمل نطاق هذه الخدمة مجموعة واسعة من الأسئلة والاستفسارات، بما في ذلك استشارات قانونية عامة، وتفسير للتشريعات، وتوجيهات حول الإجراءات القانونية، وغيرها.", True, datetime.strptime("2024-05-07 00:46:28.151237", "%Y-%m-%d %H:%M:%S.%f")),
    (2, 1, "Mensuelle", 4005, "البحث المتقدم عن القوانين الأساسي الجزائرية المنشورة في الجريدة الرسمية يعد أمرًا بالغ الأهمية للمهتمين بالقانون والقضايا القانونية في الجزائر", True, datetime.strptime("2024-05-07 00:45:41.9059", "%Y-%m-%d %H:%M:%S.%f")),
]

# Connexion à la base de données
connection = psycopg2.connect(
    dbname="easyLawDb",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)
cursor = connection.cursor()

try:
    # Insertion des données dans la table tarification
    for donnee in donnees_a_inserer:
        cursor.execute("""
            INSERT INTO public.tarification (id, "serviceId", duree, tarif, description, active, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, donnee)

    # Commit des transactions
    connection.commit()
    print("Données insérées avec succès.")

except psycopg2.Error as e:
    connection.rollback()  # Annuler toutes les opérations en cas d'erreur
    print(f"Erreur lors de l'insertion des données : {e}")

finally:
    # Fermeture de la connexion
    if cursor:
        cursor.close()
    if connection:
        connection.close()
