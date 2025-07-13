import numpy as np
import math

# ==== 1. Parámetros base ====
lat1_mean = 36.733450235      # Media latitud 1
lon1_mean = -2.890822599      # Media longitud 1
lat2_mean = 36.733855291      # Media latitud 2 (fija)
lon2_mean = -2.890259351     # Media longitud 2 (fija)

lat1_std = 0.000015788        # Desviación estándar latitud 1
lon1_std = 0.000013121        # Desviación estándar longitud 1
lat2_std = 0.000015788        # Desviación estándar latitud 2 
#lon2_std = 0.000013121        # Desviación estándar longitud 2

#lon2_start = -2.970259351    # l_i
#lon2_end = -2.810259351       # l_f (diferencia de 0.08°)
#lat2_start = 36.653855291
#lat2_end = 36.813855291        # Diferencia de 0.16° (0.08° arriba y abajo de la media)
lon2_std_start = 0.000001
lon2_std_end = 0.0001
steps = 1000
samples = 15000

#lon2_means = np.linspace(lon2_start, lon2_end, steps)
#lat2_means = np.linspace(lat2_start, lat2_end, steps)  # Valores de latitud 2 para el bucle
lon2_std_means = np.linspace(lon2_std_start, lon2_std_end, steps)  # Valores de desviación estándar de latitud 2 para el bucle
# ==== 2. Resultados ====
dist_output = []  # Archivo 1: distancias medias
uncert_output = []  # Archivo 2: incertidumbres

# ==== 3. Bucle principal Monte Carlo ====
for lon2_std in lon2_std_means:
    # Generación Monte Carlo
    lat1_samples = np.random.normal(lat1_mean, lat1_std, samples)
    lon1_samples = np.random.normal(lon1_mean, lon1_std, samples)
    lat2_samples = np.random.normal(lat2_mean, lat2_std, samples)
    lon2_samples = np.random.normal(lon2_mean, lon2_std, samples)

    # Conversión a m
    lat_km = 111320
    lon_km = 111320 * np.cos(np.radians((lat1_samples + lat2_samples) / 2))

    delta_lat = (lat2_samples - lat1_samples) * lat_km
    delta_lon = (lon2_samples - lon1_samples) * lon_km

    distances = np.sqrt(delta_lat**2 + delta_lon**2)

    dist_mean = np.mean(distances)
    dist_std = np.std(distances)

    # Distancia euclidiana con las medias
    delta_lat_det = (lat2_mean - lat1_mean) * lat_km
    avg_lat_rad = np.radians((lat1_mean + lat2_mean) / 2)
    lon_km_det = 111320 * np.cos(avg_lat_rad)
    delta_lon_det = (lon2_mean - lon1_mean) * lon_km_det

    dist_det = np.sqrt(delta_lat_det**2 + delta_lon_det**2)

    # Lugar para añadir la propagación de errores
    der_lat1=111320**2/2*(2*(lat1_mean-lat2_mean)-math.cos(math.radians(lat1_mean+lat2_mean)/2)*math.sin(math.radians(lon1_mean+lon2_mean)/2)*(lon1_mean-lon2_mean)*(lon1_mean-lon2_mean))/dist_det
    der_lat2=111320**2/2*(2*(lat2_mean-lat1_mean)-math.cos(math.radians(lat1_mean+lat2_mean)/2)*math.sin(math.radians(lon1_mean+lon2_mean)/2)*(lon1_mean-lon2_mean)*(lon1_mean-lon2_mean))/dist_det
    der_lon1=111320**2*(lon1_mean-lon2_mean)*math.cos(math.radians(lat1_mean+lat2_mean)/2)*math.cos(math.radians(lon1_mean+lon2_mean)/2)/dist_det
    der_lon2=111320**2*(lon2_mean-lon1_mean)*math.cos(math.radians(lat1_mean+lat2_mean)/2)*math.cos(math.radians(lon1_mean+lon2_mean)/2)/dist_det
    dist_uncertainty = np.sqrt(der_lat1**2*lat1_std**2+der_lat2**2*lat2_std**2 + der_lon1**2*lon1_std**2+der_lon2**2*lon2_std**2)

    # ==== 4. Guardar resultados ====
    dist_output.append(f"{lon2_std:.6f}\t{dist_mean:.6f}\t{dist_det:.6f}\n")
    uncert_output.append(f"{lon2_std:.6f}\t{dist_std:.6f}\t{dist_uncertainty:.6f}\n")

# ==== 5. Escritura a archivos ====
with open("distancias_medias.txt", "w") as f1:
    f1.writelines(dist_output)

with open("incertidumbres.txt", "w") as f2:
    f2.writelines(uncert_output)
