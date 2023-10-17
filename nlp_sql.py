## Key with paid service

import openai
import panel as pn
openai.api_key="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"



def continue_conversation(messages, temperature=0):
    
    response = openai.ChatCompletion.create( 
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=temperature, 
    )

    return response.choices[0].message["content"]

# def continue_conversation(natural_language_query):
#     response = openai.Completion.create(
#         engine="davinci",
#         prompt=f"Translate the following natural language query into SQL: {natural_language_query}",
#         max_tokens=50,  # You can adjust this as needed
#         stop=None,  # You can add a stop word if needed
#         temperature=0.7  # You can adjust this to control the randomness of the output
#     )
#     return response.choices[0].text

context = [{'role':'system', 'content':"""
you are a bot to assist in create SQL commands, all your answers should start with \
this is your SQL, and after that an SQL that can do what the user request. \
Your Database is composed by a SQL database with some tables. \
Try to Maintain the SQL order simple.
Put the SQL command in white letters with a black background, and just after \
a simple and concise text explaining how it works. 
If the user ask for something that can not be solved with an SQL Order \
just answer something nice and simple and ask him for something that \
can be solved with SQL. 
"""}]

context.append( {'role':'system', 'content':"""
first table: 
{
  "tableName": "employees",
  "fields": [
    {
      "nombre": "ID_usr",
      "tipo": "int"
    },
    {
      "nombre": "name",
      "tipo": "string"
    }
  ]
}
"""
})

context.append( {'role':'system', 'content':"""
second table: 
{
  "tableName": "salary",
  "fields": [
    {
      "nombre": "ID_usr",
      "type": "int"
    },
    {
      "yt": "year",
      "type": "date"
    },
    {
      "sal": "salary",
      "type": "float"
    }
  ]
}
"""
})

context.append( {'role':'system', 'content':"""
third table: 
{
  "tablename": "studies",
  "fields": [
    {
      "name": "ID",
      "type": "int"
    },
    {
      "ee": "ID_usr",
      "type": "int"
    },
    {
      "edu": "educational level",
      "type": "int"
    },
    {
      "name": "Institution",
      "type": "string"
    },
    {
      "yr": "Years",
      "type": "date"
    }
    {
      "spl": "Speciality",
      "type": "string"
    }
  ]
}

"""
})

# msg="select empyoyees whoses education level is Masters"
msg="select empyoyees nombre whose sal is 30000 and ans have studied in the yr 2003"
# ww=continue_conversation(msg)


