
CREATE TABLE [Levels]
(
 [ID_Level] INTEGER NOT NULL PRIMARY KEY,
 [Label]    TEXT NOT NULL
);

CREATE TABLE [Classrooms]
(
 [ID_Classroom] INTEGER NOT NULL PRIMARY KEY,
 [Label]    TEXT NOT NULL
);

CREATE TABLE [Professors]
(
 [ID_Professor] INTEGER NOT NULL PRIMARY KEY,
 [Name]       	TEXT NOT NULL
);

CREATE TABLE [Classes]
(
 [ID_Class] INTEGER NOT NULL PRIMARY KEY,
 [Label]    TEXT NOT NULL ,
 [ID_Level] INTEGER NOT NULL ,

 FOREIGN KEY ([ID_Level])
       REFERENCES [Levels]([ID_Level])
);

CREATE TABLE [Modules]
(
 [ID_Module] INTEGER NOT NULL PRIMARY KEY,
 [Label]     TEXT NOT NULL ,
 [ID_Level]  INTEGER NOT NULL ,

 FOREIGN KEY ([ID_Level])
       REFERENCES [Levels]([ID_Level])
);


CREATE TABLE [Students]
(
 [ID_Student] INTEGER NOT NULL ,
 [Name]       TEXT NOT NULL ,
 [CNE]        TEXT NOT NULL ,
 [ID_Class]   INTEGER NOT NULL ,

  PRIMARY KEY ([ID_Student], [CNE])
  FOREIGN KEY ([ID_Class])
       REFERENCES [Classes]([ID_Class])
);

CREATE TABLE [Seances]
(
 [ID_Seance]   INTEGER NOT NULL PRIMARY KEY,
 [ID_Classroom]   INTEGER NOT NULL ,
 [Date]        TEXT NOT NULL ,
 [Starting_hour] INTEGER NOT NULL ,
 [Ending_hour]    INTEGER NOT NULL ,
 [ID_Module]   INTEGER NOT NULL ,
 [ID_Class]    INTEGER NOT NULL ,
 [ID_Professor] INTEGER NOT NULL ,

  FOREIGN KEY ([ID_Module])
       REFERENCES [Modules]([ID_Module])

  FOREIGN KEY ([ID_Class])
       REFERENCES [Classes]([ID_Class])

  FOREIGN KEY ([ID_Classroom])
       REFERENCES [Classrooms]([ID_Classroom])

  FOREIGN KEY ([ID_Professor])
       REFERENCES [Professors]([ID_Professor])
);

CREATE TABLE [Presences]
(
 [ID_Presence] INTEGER NOT NULL PRIMARY KEY,
 [ID_Student]   INTEGER NOT NULL ,
 [ID_Seance]    INTEGER NOT NULL ,

  FOREIGN KEY ([ID_Student])
       REFERENCES [Students]([ID_Student])

   FOREIGN KEY ([ID_Seance])
       REFERENCES [Seances]([ID_Seance])
);