# Soluciones

## Requisitos

- [sqlite](https://www.sqlite.org/download.html)

## Ejercicio 1

1. Iniciar sesión en sqlite:
    ```
    sqlite3
    ```

2. Importar los datos:
    ```
    .read dataset_3.sql
    ```

    Validar que las tablas han sido creadas:
    ```
    .tables
    ```

    Deberías ver algo similar a:
    ```
    sqlite> .tables
    ages                 exercise             pediatric          
    data_collection_day  participants         thanatol
    ```

3. Crear la vista con los datos combinados:
    ```sql
    create view all_participants as

        select
            age as age,
            hours_per_day as hours_per_day,
            mmol_per_l as mmol_per_l
        from
            pediatric

        union all

        select
            (
                julianday((select data_collection_day from data_collection_day limit 1))
                - julianday(ages.birthday)
            ) / 365.25 as age,
            (exercise.hours_per_week / 7) as hours_per_day,
            thanatol.mmol_per_l as mmol_per_l
        from
            participants
                inner join ages on participants.id = ages.id
                inner join exercise on participants.id = exercise.id
                inner join thanatol on participants.id = thanatol.id;
    ```

    Validar que el número total de filas de `all_participants` es la suma de las tablas `participants` y `pediatric`:

    ```
    sqlite> select count(*) from participants;
    963
    sqlite> select count(*) from pediatric;
    37
    sqlite> select count(*) from all_participants;
    1000
    ```

### Referencias

- [Date And Time Functions](https://www.sqlite.org/lang_datefunc.html)
- [sqlite - difference of year between two date - Stack Overflow](https://stackoverflow.com/a/36918703)
- [SQLite date() Function By Practical Examples](https://www.sqlitetutorial.net/sqlite-date-functions/sqlite-date-function/)
- [SQLite UNION with Examples, UNION vs. UNION ALL](https://www.sqlitetutorial.net/sqlite-union/)
- [What is the difference between full outer join and union in SQL?](https://www.quora.com/What-is-the-difference-between-full-outer-join-and-union-in-SQL)

### Ejercicio 2

1. Ejecutar los pasos del [Ejercicio 1](#ejercicio-1) y dejar la sesión abierta.

2. Activar las cabeceras en sqlite:
    ```
    .headers on
    ```

3. Configurar el `output mode` para que sea **CSV**:
    ```
    .mode csv
    ```

4. Enviar el `output` al fichero `all_participants.csv`:
    ```
    .output all_participants.csv
    ```

5. Ejecutar la query:
    ```sql
    select * from all_participants;
    ```

6. Salir de sqlite:
    ```
    .exit
    ```

Deberías ver el fichero `all_participants.csv` en el directorio.

Nota: fíjate que el fichero con este nombre ya está en el repositorio como parte de la solución, para validar que las indicaciones funcionan puedes cambiar el nombre del archivo en el paso 4.

### Referencias

- [Export SQLite Database to a CSV file using sqlite3 command line tool (Ubuntu 16.04)](https://deeplearning.lipingyang.org/export-sqlite-database-to-a-csv-file-using-sqlite3-command-line-tool-ubuntu-16-04/)
