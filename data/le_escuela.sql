-- ----------------------------
-- Table structure for le_ciclo
-- ----------------------------
IF EXISTS (SELECT * FROM sys.all_objects WHERE object_id = OBJECT_ID(N'[sva].[le_ciclo]') AND type IN ('U'))
	DROP TABLE [sva].[le_ciclo]
GO

CREATE TABLE [sva].[le_ciclo] (
  [id] int  IDENTITY(1,1) NOT NULL,
  [numeracion] varchar(30) COLLATE Modern_Spanish_CI_AS  NULL,
  [parent] int  NULL,
  [idescparent] varchar(8) COLLATE Modern_Spanish_CI_AS  NULL,
  [idciclo] varchar(4) COLLATE Modern_Spanish_CI_AS  NULL
)
GO

ALTER TABLE [sva].[le_ciclo] SET (LOCK_ESCALATION = TABLE)
GO


-- ----------------------------
-- Table structure for le_cursos
-- ----------------------------
IF EXISTS (SELECT * FROM sys.all_objects WHERE object_id = OBJECT_ID(N'[sva].[le_cursos]') AND type IN ('U'))
	DROP TABLE [sva].[le_cursos]
GO

CREATE TABLE [sva].[le_cursos] (
  [id] int  IDENTITY(1,1) NOT NULL,
  [nombrecompleto] varchar(255) COLLATE Modern_Spanish_CI_AS  NULL,
  [nombrecorto] varchar(255) COLLATE Modern_Spanish_CI_AS  NULL,
  [categoriaid] int  NULL,
  [fechainicio] bigint  NULL,
  [semestre] varchar(8) COLLATE Modern_Spanish_CI_AS  NULL,
  [idcurso] varchar(50) COLLATE Modern_Spanish_CI_AS  NULL,
  [id_moodle] int  NULL
)
GO

ALTER TABLE [sva].[le_cursos] SET (LOCK_ESCALATION = TABLE)
GO


-- ----------------------------
-- Table structure for le_escuela
-- ----------------------------
IF EXISTS (SELECT * FROM sys.all_objects WHERE object_id = OBJECT_ID(N'[sva].[le_escuela]') AND type IN ('U'))
	DROP TABLE [sva].[le_escuela]
GO

CREATE TABLE [sva].[le_escuela] (
  [id] int  IDENTITY(1,1) NOT NULL,
  [semestre] int  NULL,
  [numeracion] varchar(20) COLLATE Modern_Spanish_CI_AS  NULL,
  [parent] int  NULL,
  [idesc] varchar(8) COLLATE Modern_Spanish_CI_AS  NULL
)
GO

ALTER TABLE [sva].[le_escuela] SET (LOCK_ESCALATION = TABLE)
GO


-- ----------------------------
-- Table structure for le_facultad
-- ----------------------------
IF EXISTS (SELECT * FROM sys.all_objects WHERE object_id = OBJECT_ID(N'[sva].[le_facultad]') AND type IN ('U'))
	DROP TABLE [sva].[le_facultad]
GO

CREATE TABLE [sva].[le_facultad] (
  [id] int  IDENTITY(1,1) NOT NULL,
  [semestre] int  NULL,
  [numeracion] varchar(20) COLLATE Modern_Spanish_CI_AS  NULL,
  [parent] int  NULL,
  [idfac] varchar(8) COLLATE Modern_Spanish_CI_AS  NULL
)
GO

ALTER TABLE [sva].[le_facultad] SET (LOCK_ESCALATION = TABLE)
GO


-- ----------------------------
-- Table structure for le_semestre
-- ----------------------------
IF EXISTS (SELECT * FROM sys.all_objects WHERE object_id = OBJECT_ID(N'[sva].[le_semestre]') AND type IN ('U'))
	DROP TABLE [sva].[le_semestre]
GO

CREATE TABLE [sva].[le_semestre] (
  [id] int  IDENTITY(1,1) NOT NULL,
  [nombre] varchar(10) COLLATE Modern_Spanish_CI_AS  NULL,
  [nombre_completo] varchar(50) COLLATE Modern_Spanish_CI_AS  NULL,
  [descripcion] varchar(255) COLLATE Modern_Spanish_CI_AS  NULL,
  [parent] int  NULL
)
GO

ALTER TABLE [sva].[le_semestre] SET (LOCK_ESCALATION = TABLE)
GO


-- ----------------------------
-- Auto increment value for le_ciclo
-- ----------------------------
DBCC CHECKIDENT ('[sva].[le_ciclo]', RESEED, 208)
GO


-- ----------------------------
-- Primary Key structure for table le_ciclo
-- ----------------------------
ALTER TABLE [sva].[le_ciclo] ADD CONSTRAINT [PK__le_escue__3213E83F37CAEB01] PRIMARY KEY CLUSTERED ([id])
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)  
ON [PRIMARY]
GO


-- ----------------------------
-- Auto increment value for le_cursos
-- ----------------------------
DBCC CHECKIDENT ('[sva].[le_cursos]', RESEED, 1252)
GO


-- ----------------------------
-- Auto increment value for le_escuela
-- ----------------------------
DBCC CHECKIDENT ('[sva].[le_escuela]', RESEED, 27)
GO


-- ----------------------------
-- Primary Key structure for table le_escuela
-- ----------------------------
ALTER TABLE [sva].[le_escuela] ADD CONSTRAINT [PK__le_escue__3213E83F87514117] PRIMARY KEY CLUSTERED ([id])
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)  
ON [PRIMARY]
GO


-- ----------------------------
-- Auto increment value for le_facultad
-- ----------------------------
DBCC CHECKIDENT ('[sva].[le_facultad]', RESEED, 11)
GO


-- ----------------------------
-- Primary Key structure for table le_facultad
-- ----------------------------
ALTER TABLE [sva].[le_facultad] ADD CONSTRAINT [PK__facultad__3213E83FC0C42CFA] PRIMARY KEY CLUSTERED ([id])
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)  
ON [PRIMARY]
GO


-- ----------------------------
-- Auto increment value for le_semestre
-- ----------------------------
DBCC CHECKIDENT ('[sva].[le_semestre]', RESEED, 10)
GO


-- ----------------------------
-- Primary Key structure for table le_semestre
-- ----------------------------
ALTER TABLE [sva].[le_semestre] ADD CONSTRAINT [PK__le_semes__3213E83F6EAD3301] PRIMARY KEY CLUSTERED ([id])
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)  
ON [PRIMARY]
GO


-- ----------------------------
-- Foreign Keys structure for table le_escuela
-- ----------------------------
ALTER TABLE [sva].[le_escuela] ADD CONSTRAINT [FK__le_escuel__semes__71800FB2] FOREIGN KEY ([semestre]) REFERENCES [sva].[le_semestre] ([id]) ON DELETE NO ACTION ON UPDATE NO ACTION
GO


-- ----------------------------
-- Foreign Keys structure for table le_facultad
-- ----------------------------
ALTER TABLE [sva].[le_facultad] ADD CONSTRAINT [semestre] FOREIGN KEY ([semestre]) REFERENCES [sva].[le_semestre] ([id]) ON DELETE NO ACTION ON UPDATE NO ACTION
GO


-- Insercion de datos a la tabla le_curso desde los cursosprogramados
INSERT INTO sva.le_cursos (nombrecompleto, nombrecorto, categoriaid, fechainicio, semestre, idcurso)
SELECT DISTINCT
	concat ( cp.Semestre, ', ', c.Nombre, ', ', c.Curricula, ', ', e.Abreviatura, ', ', cp.Seccion ) AS nombrecompleto,
	concat ( c.Nombre, ', ', e.Abreviatura, ', ', c.Curricula, ', ', cp.Semestre, ', ', cp.Seccion ) AS nombrecorto,
	lc.parent AS categoriaid,
	DATEDIFF( SECOND, '1970-01-01 00:00:00.0', '2023-04-26 00:00:00.0' ) AS fechainicio,
	cp.Semestre,
-- 	concat ( cp.Semestre, '-', le.idesc, '-', c.Curricula, '-', cp.Seccion, '-', c.Curso ) AS idcurso,
	concat ( cp.Semestre, '-', CAST ( c.id AS VARCHAR ), '-', CAST ( cp.CursoProgramado AS VARCHAR )) AS idcurso
FROM
	dbo.CursoProgramado AS cp
	INNER JOIN dbo.Curso AS c ON cp.Curricula = c.Curricula 
	AND cp.Curso = c.Curso 
	AND cp.Escuela = c.Escuela
	INNER JOIN sva.le_escuela AS le ON c.Escuela = le.idesc
	INNER JOIN sva.le_ciclo AS lc ON le.parent = lc.idescparent 
	AND c.Ciclo = lc.idciclo
	INNER JOIN dbo.Escuela AS e ON c.Escuela = e.Escuela
	INNER JOIN sva.le_semestre AS ls ON le.semestre = ls.id 
	AND cp.Semestre = ls.nombre 
WHERE
	cp.Semestre = '2020-1' and cp.tipo != 'H';
	

-- Timestamp to date
SELECT DATEADD(SECOND, 1682553540, '1970-01-01 00:00:00.0')


-- Date to timestamp
SELECT DATEDIFF(SECOND, '1970-01-01 00:00:00.0', '2023-04-26 23:59:00.0')


-- Procedimiento para retornar los matriculados

CREATE PROCEDURE le_matriculados (@semestre varchar(10), @estudiante varchar(20) = NULL)
AS
BEGIN	
		
		IF ISNULL(@estudiante, '') = ''
    BEGIN
        SELECT LOWER
					( r.Alumno ) AS alumno,
					concat ( c.Nombre, ', ', e.Abreviatura, ', ', cp.Semestre, ', ', cp.Seccion ) AS idcurso 
					INTO #matricula_total
				FROM
					dbo.Rendimiento AS r
					INNER JOIN dbo.Curso AS c ON r.Curricula = c.Curricula 
					AND r.Curso = c.Curso 
					AND r.Escuela = c.Escuela
					INNER JOIN dbo.CursoProgramado AS cp ON c.Curricula = cp.Curricula 
					AND c.Curso = cp.Curso 
					AND c.Escuela = cp.Escuela 
					AND r.Semestre = cp.Semestre 
					AND r.Seccion = cp.Seccion
					INNER JOIN dbo.Escuela AS e ON cp.Escuela = e.Escuela 
				WHERE
					r.Semestre = @semestre
					
					
				SELECT
					lc.id_moodle AS curso_id,
					a.moodle_id AS alumno_id 
				FROM
					#matricula_total m
					INNER JOIN sva.le_cursos lc ON lc.nombrecorto = m.idcurso
					INNER JOIN dbo.Alumno a ON m.alumno = a.Alumno
					
					
				DROP TABLE IF EXISTS #matricula_total;
				
    END
    ELSE
    
		BEGIN
        SELECT LOWER
					( r.Alumno ) AS alumno,
					concat ( c.Nombre, ', ', e.Abreviatura, ', ', cp.Semestre, ', ', cp.Seccion ) AS idcurso
					INTO #matricula_alumno
				FROM
					dbo.Rendimiento AS r
					INNER JOIN dbo.Curso AS c ON r.Curricula = c.Curricula 
					AND r.Curso = c.Curso 
					AND r.Escuela = c.Escuela
					INNER JOIN dbo.CursoProgramado AS cp ON c.Curricula = cp.Curricula 
					AND c.Curso = cp.Curso 
					AND c.Escuela = cp.Escuela 
					AND r.Semestre = cp.Semestre 
					AND r.Seccion = cp.Seccion
					INNER JOIN dbo.Escuela AS e ON cp.Escuela = e.Escuela 
				WHERE
					r.Semestre = @semestre
					and r.Alumno = @estudiante;
					
				SELECT
					lc.id_moodle AS curso_id,
					a.moodle_id AS alumno_id 
				FROM
					#matricula_alumno m
					INNER JOIN sva.le_cursos lc ON lc.nombrecorto = m.idcurso
					INNER JOIN dbo.Alumno a ON m.alumno = a.Alumno;
					
				
				DROP TABLE IF EXISTS #matricula_alumno
    END
END

-- Busqueda de estudiantes sin matricula

DROP TABLE IF EXISTS #matricula_moodle; 
DROP TABLE IF EXISTS #matricula_sga;

SELECT
	lm.curso_id,
	lm.alumno_id 
-- 	INTO #matricula_moodle 
FROM
	sva.le_maticulas_moodle lm 
WHERE 
	lm.semestre_id = 15
GROUP BY
	lm.curso_id,
	lm.alumno_id;
	

CREATE TABLE #matricula_sga ( curso_id INT, alumno_id INT );

INSERT INTO #matricula_sga EXEC le_matriculados '2019-1';

SELECT
	ms.curso_id AS curso_sga,
	ms.alumno_id AS alumno_sga,
	mm.curso_id AS curso_moodle,
	mm.alumno_id AS alumno_moodle 
FROM
	#matricula_sga ms
	LEFT JOIN #matricula_moodle mm 
	ON ms.curso_id = mm.curso_id 
	AND ms.alumno_id = mm.alumno_id 
WHERE
	mm.alumno_id IS NULL;
	

SELECT
	s.curso_id,
	s.alumno_id,
	m.curso_id,
	m.alumno_id
FROM
	#matricula_sga AS s
	RIGHT JOIN #matricula_moodle AS m ON s.curso_id = m.curso_id 
	AND s.alumno_id = m.alumno_id 
WHERE
	s.curso_id IS NULL 
	AND s.alumno_id IS NULL;



-- Eliminando la vista le_correolimpio y creando un procedimiento
CREATE PROCEDURE le_datos_matriculados (@semestre VARCHAR(10))
AS
BEGIN
    SELECT DISTINCT LOWER
			( r.Alumno ) AS alumno,
			TRIM ( a.Password ) AS password,
			TRIM ( a.Nombre ) AS nombre,
			CONCAT ( TRIM ( a.ApellidoPaterno ), ' ', TRIM ( a.ApellidoMaterno ) ) AS apellido,
			REPLACE( a.Email, ' ', '' ) AS email
			INTO #correo_limpio
		FROM
			dbo.Rendimiento AS r
			INNER JOIN dbo.Alumno AS a ON r.Alumno = a.Alumno 
		WHERE
			r.Semestre = @semestre
			
			
		SELECT DISTINCT
			a.alumno,
			a.password,
			a.nombre,
			a.apellido,
			a.email 
		FROM
			#correo_limpio AS a 
		WHERE
			( a.email <> '' OR a.email IS NULL ) 
			AND CHARINDEX( '@', a.email ) > 0 
			AND CHARINDEX( '.', a.email, CHARINDEX( '@', a.email ) ) > 0 
			AND CHARINDEX( ' ', a.email ) = 0 
			AND PATINDEX( '%[,"()<>;[]]%', a.email ) = 0 
		GROUP BY
			a.email,
			a.alumno,
			a.password,
			a.nombre,
			a.apellido
			
			
		DROP TABLE IF EXISTS #correo_limpio
			
END
