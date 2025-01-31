# TA06-Group1

## E02: Organitzar i processar les dades

Los encabezados están separados por tabulaciones, su significado es:
precip: Indica que los datos son de precipitaciones.
MIROC5: Es el modelo climático utilizado para simular las precipitaciones.
RCP60: Representa el escenario de concentración de gases (RCP 6.0).
REGRESION: método estadístico usado para ajustar o procesar los datos.
decimas: Indica que los valores de precipitaciones están en decimas de milimetro (10 = 1mm).

Los datos están separados por espacios. La primera columna es un identificador de la estación meteorológica o el punto geográfico de simulación. La segunda columna es el año, la tercera el mes y las restantes son el día.

 **En cada script se ha documentado, añadiendo líneas de comentarios.**
Los valores nulos se han identificado como -999 y hemos decidido que el código lo trate como datos ausentes.
Los datos que no se podían convertir en formato numéricos (por ejemplo el encabezado) se han ignorado automáticamente al procesar las columnas.

- 1. Índice de Estacionalidad
Es la variación periódica y predecible de la misma con un periodo inferior o igual a un año.Su objetivo es identificar cuán irregulares son las lluvias a lo largo del año.

- 2. Duración Máxima de Sequías
Identifica el período continuo más largo sin precipitaciones significativas (días secos) en un año.
(Ambos en el mismo script)
