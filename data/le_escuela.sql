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
-- Auto increment value for le_escuela
-- ----------------------------
DBCC CHECKIDENT ('[sva].[le_escuela]', RESEED, 135)
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
DBCC CHECKIDENT ('[sva].[le_facultad]', RESEED, 59)
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
DBCC CHECKIDENT ('[sva].[le_semestre]', RESEED, 7)
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

