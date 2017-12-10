@echo off
set JAVA_HOME="C:\Program Files (x86)\Java\jre1.8.0_111"


set CUR_DIR=%CD%

cd src/hebrewNER


set CP="%CUR_DIR%/;%CUR_DIR%/jars/opennlp.jar;%CUR_DIR%/jars/gnu.jar;%CUR_DIR%/jars/tagger.jar"

set CMP_CMD=%JAVA_HOME%\bin\javacpl.exe -cp %CP%


echo Building hebrewNER.io...
cd io
%CMP_CMD% -d ../../../ *.java
cd ..
echo Done

echo Building hebrewNER.util...
cd util
%CMP_CMD% -d ../../../ *.java
cd ..
echo Done

echo Building hebrewNER.maxent...
cd maxent
%CMP_CMD% -d ../../../ *.java
cd ..
echo Done

echo Building hebrewNER.hmm...
cd hmm 
%CMP_CMD% -d ../../../ *.java
cd ..
echo Done

echo Building hebrewNER.baseline...
cd baseline
%CMP_CMD% -d ../../../ *.java
cd ..
echo Done

echo Building hebrewNER.sentenceDetect...
cd sentenceDetect
%CMP_CMD% -d ../../../ *.java
cd ..
echo Done

echo Building hebrewNER...
%CMP_CMD% -d ../../ *.java
echo Done

cd ..\..
