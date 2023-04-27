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
SELECT
	concat ( cp.Semestre, ', ', c.Nombre, ', ', e.Abreviatura, ', ', cp.Seccion ) AS nombrecompleto,
	concat ( c.Nombre, ', ', e.Abreviatura, ', ', cp.Semestre, ', ', cp.Seccion ) AS nombrecorto,
	lc.parent as categoriaid,
	DATEDIFF(SECOND, '1970-01-01 00:00:00.0', '2023-04-26 00:00:00.0') as fechainicio,
	cp.Semestre,
	concat (cp.Semestre, '-', le.idesc, c.Curricula, cp.Seccion, '-', c.Curso) as idcurso
FROM
	dbo.CursoProgramado AS cp
	INNER JOIN dbo.Curso AS c ON cp.Curricula = c.Curricula 
	AND cp.Curso = c.Curso 
	AND cp.Escuela = c.Escuela
	INNER JOIN sva.le_escuela AS le ON c.Escuela = le.idesc
	INNER JOIN sva.le_ciclo AS lc ON le.parent = lc.idescparent 
	AND c.Ciclo = lc.idciclo
	INNER JOIN dbo.Escuela AS e ON c.Escuela = e.Escuela 
WHERE
	cp.Semestre = '2020-1'


-- Timestamp to date
SELECT DATEADD(SECOND, 1682553540, '1970-01-01 00:00:00.0')


-- Date to timestamp
SELECT DATEDIFF(SECOND, '1970-01-01 00:00:00.0', '2023-04-26 23:59:00.0')
