import psycopg2

try:
    con = psycopg2.connect(
        host = "172.22.0.2",
        database='postgres',
        user='postgres',
        password='OpenCV'
    )
except:
    print('connection failed!')
    con = None

cur = con.cursor()

cur.execute("""
CREATE OR REPLACE FUNCTION public.vec_sub(arr1 double precision[], arr2 double precision[])
 RETURNS double precision[]
 LANGUAGE sql
 STRICT
AS $function$	
SELECT array_agg (result)
    FROM (SELECT (tuple.val1 - tuple.val2) * (tuple.val1 - tuple.val2)
        AS result
        FROM (SELECT UNNEST ($1) AS val1
               , UNNEST ($2) AS val2
               , generate_subscripts ($1, 1) AS ix) tuple
    ORDER BY ix) inn;
	
	$function$

""")
cur.execute('''
CREATE OR REPLACE FUNCTION public.euclidian(arr1 double precision[], arr2 double precision[])
 RETURNS double precision
 LANGUAGE sql
AS $function$
select sqrt (SUM (tab.v)) as euclidian from (SELECT
     UNNEST (vec_sub (arr1, arr2)) as v) as tab;
	 $function$

''')

cur.execute('''
CREATE TABLE public.face_table
(
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    face_embedding double precision[] NOT NULL,
    PRIMARY KEY (id)
);
'''
)

con.commit()