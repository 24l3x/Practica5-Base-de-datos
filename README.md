# Practica5-Base-de-datos
## Edición de valores de una base de datos relacional empleando DML
### Ejercicios:
#### 1. ✅ 2. ✅ 3.✅

***Orden***
	
	practica5/
    ├── docker-compose.yml
    ├── Dockerfile
    ├── entrypoint.sh
    ├── requirements.txt
    ├── sql/
    │   └── init.sql     
    └── scripts/
        ├── poblar_leve.py
        ├── poblar_moderado.py
        └── poblar_masivo.py


### Ejercicio 1
#### MER
![MER](https://github.com/user-attachments/assets/0998288f-59a3-4053-a1f4-c84d26f83d55)
**DDL en carpeta sql**

### Ejercicio 2
#### Capturas Ejecución
##### Nivel 1
![Leve](https://github.com/user-attachments/assets/3dd90922-4dce-42cd-9501-4a1853754215)

    $env:NIVEL_POBLADO="leve"; docker-compose up --build


##### Nivel 2
![Moderado](https://github.com/user-attachments/assets/fe9993fc-2878-4957-be36-4da08ed8a647)

    $env:NIVEL_POBLADO="moderado"; docker-compose up --build

##### Nivel 3
<img width="682" height="280" alt="Masivo" src="https://github.com/user-attachments/assets/645b9258-ff2f-422a-93b5-05cf1a4a0d68" />

    $env:NIVEL_POBLADO="masivo"; docker-compose up --build

###### Si el poblador se traba o no llena la base de datos correctamente, reinicialo

    docker-compose restart poblador

###### Asi mismo recuerda que cada vez que cargues un nuevo poblador debes bajar el docker compose Y BORRAR los volumenes

    docker-compose down -v

#### Tabla Comparativa
|  Metrica | Nivel 1 | Nivel 2 | Nivel 3  |
| ------------ | ------------ | ------------ | ------------ |
| Total de registros  | 500  | 88,068  | 1,060,022  |
| Tiempo de ejecución  | 0.5s | 25.3s  | 34.23s  |
| Resgistros/segundo  | 1,000  | 3,480.95  | 30,967.64  |
| Uso de memoria (MB) | 518.43 Mb  | 414.43 Mb  | 504 Mb  |
| Tamaño de BD (MB) | 0.2 Mb  | 9.08 Mb  | 91.53 Mb  |

##### SQL para Total de registros y Tamaño de BD
###### Total de registros
```sql
SELECT 
    (SELECT COUNT(*) FROM Cliente) +
    (SELECT COUNT(*) FROM Productos) +
    (SELECT COUNT(*) FROM Pedido) +
    (SELECT COUNT(*) FROM Detalle_Pedido) +
    (SELECT COUNT(*) FROM Pagos) AS "Total Registros Insertados";
```
###### Tamaño de BD
```sql
SELECT 
    table_schema AS "Base de Datos", 
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS "Tamaño (MB)" 
FROM information_schema.TABLES 
WHERE table_schema = 'tienda_abarrotes';
```
### Ejercicio 3
#### 3.1
**El codigo de cada imagen se encuentran en la carpeta *SQL>DML>DML.sql***
- 3.1.1
<img width="1048" height="708" alt="image" src="https://github.com/user-attachments/assets/aff9b562-8387-4800-8cfc-9e37eead3659" />

- 3.1.2
<img width="365" height="698" alt="image" src="https://github.com/user-attachments/assets/0bcac0c7-8b70-41a6-b2cc-acff35262424" />

- 3.1.4
<img width="653" height="713" alt="image" src="https://github.com/user-attachments/assets/30ab43c0-c963-43e2-87c9-a4b5d977ea76" />

- 3.1.6
<img width="578" height="642" alt="image" src="https://github.com/user-attachments/assets/2ee301be-9608-4364-84c6-7aca89ad575f" />

- 3.1.7
<img width="652" height="794" alt="image" src="https://github.com/user-attachments/assets/42869732-630c-4678-a6c7-068ed55c2983" />

- 3.1.10
<img width="764" height="776" alt="image" src="https://github.com/user-attachments/assets/f062aaa6-0961-40d4-b832-c8cc50743e5a" />

#### 3.2

- 3.2.2
<img width="1536" height="246" alt="image" src="https://github.com/user-attachments/assets/a15ca27a-4f0a-4e86-87c0-bdd6ce73b3fc" />

- 3.2.3
<img width="1540" height="210" alt="image" src="https://github.com/user-attachments/assets/e8ccb026-7b2a-48d2-8149-c12e3a1b2eb9" />

- 3.2.4
<img width="1530" height="194" alt="image" src="https://github.com/user-attachments/assets/f7ffa44a-5e1e-4a3c-93e9-7e08f9371270" />

#### 3.3

- 3.3.1
<img width="1507" height="678" alt="image" src="https://github.com/user-attachments/assets/946f8c0f-87ba-4e62-b387-a728a7bb1dd5" />

- 3.3.2
<img width="1536" height="178" alt="image" src="https://github.com/user-attachments/assets/5984d287-2e86-47d2-9e0f-5d6fe3c1d515" />

- 3.3.3
<img width="1533" height="172" alt="image" src="https://github.com/user-attachments/assets/0795b83c-35c8-4bb3-b6a0-7c749ef9bdae" />

- 3.3.4
<img width="1535" height="184" alt="image" src="https://github.com/user-attachments/assets/4d0a6eae-f104-4722-ba45-bcb42a4ba64b" />


### Ejercicio 4
** Todos los archivos para la dockerizacion estan en la carpeta practica5 **
