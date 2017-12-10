@echo off


set JAVA_HOME="C:\Program Files (x86)\Java\jre1.8.0_111"

set CUR_DIR=%CD%

set CP="%CUR_DIR%/;%CUR_DIR%/jars/opennlp.jar;%CUR_DIR%/jars/gnu.jar;%CUR_DIR%/jars/tagger.jar"

%JAVA_HOME%\bin\java.exe -Xmx1G -cp %CP% hebrewNER.Main %1



