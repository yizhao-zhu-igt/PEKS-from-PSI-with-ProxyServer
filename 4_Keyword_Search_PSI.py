import json
import time
import random
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import logging
import os
import re

# Set up logging file
log_file = '4_Keyword_Search_PSI.log'
if os.path.exists(log_file):
    os.remove(log_file)
# Set up logging
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def load_public_params():
    with open('public_params.json', 'r') as file:
        public_params = json.load(file)
    return public_params['p'], public_params['q'], public_params['g'], public_params['h']

def load_ps_data(i):
    with open(f'ps_{i}_data.json', 'r') as file:
        ps_data = json.load(file)
    return ps_data['K'], ps_data['X'], ps_data['F_coeffs']

def load_y():
    with open('Y.json', 'r') as file:
        Y = json.load(file)
    return Y

def H3(binary_string, q):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(binary_string)
    hash_bytes = digest.finalize()
    hash_int = int.from_bytes(hash_bytes, byteorder='big')
    return pow(hash_int, 1, q)

def hex_to_binary(hex_string):
    return bin(int(hex_string, 16))[2:].zfill(256)

def evaluate_polynomial(coeffs, x, q):
    result = 0
    for i, coeff in enumerate(coeffs):
        result += int(coeff, 16) * pow(x, i, q)
    result += pow(x, len(coeffs), q)
    return result % q

def main():
    # Set the filename pattern
    pattern = r'ps_\d{1,10}_data.json'
    # Count the number of files
    total_count = 0
    for filename in os.listdir(os.getcwd()):
        if re.match(pattern, filename):
            loginfo = f"Found file: {filename}"
            logging.info(loginfo)
            #print(loginfo)
            total_count += 1
    logging.info(f"------Keyword search Start------")
    start_time = time.time()
    logging.info(f"Load public params")
    p, q, g, h = load_public_params()
    Y = load_y()
    logging.info(f"------Load Y------")
    intersection = set()

    random_ps_index = random.randint(1, total_count)
    logging.info("Randomly Choose Proxy Server, Proxy Serer Index {random_ps_index}.")
    for i in range(random_ps_index, random_ps_index + 1):
        logging.info("Loading PS Data from ps_{random_ps_index}_data.json.")
        K, X, F_coeffs = load_ps_data(i)

        # DU: Convert Y to binary strings
        Y_binary = {key: hex_to_binary(value) for key, value in Y.items()}

        # PS_i: Convert X to binary strings
        X_binary = {key: hex_to_binary(value) for key, value in X.items()}

        # DU: Compute ct_j and t_j
        logging.info("Compute ct_j and t_j")
        t = {}
        for j in range(1, len(Y_binary) + 1):
            y_tilde = H3(Y_binary[f'y_{j}'].encode(), q)
            ct_j = 1
            for k in range(len(K)):
                ct_j *= pow(int(K[k], 16), pow(y_tilde, k, q), q)
            ct_j *= pow(g * h, pow(y_tilde, len(K), q), q)
            #ct_j %= q

            s_j = random.randint(1, q - 1)
            t_j1 = pow(g, s_j, q)
            t_j2 = pow(ct_j, s_j, q)
            t[f't_{j}'] = (t_j1, t_j2)

        logging.info("Perform keyword search")
        # PS_i: Perform keyword search
        for u in range(1, len(Y_binary) + 1):
            x_tilde = H3(X_binary[f'x_{u}^({i})'].encode(), q)
            for j in range(1, 2):
                t_j1, t_j2 = t[f't_{j}']
                F_x = evaluate_polynomial(F_coeffs, x_tilde, q)
                if t_j2 == pow(t_j1, F_x, q):
                    intersection.add(f'x_{u}^({i})')

        # Check if the intersection is not empty
        if intersection:
            break
    logging.info(f"------Keyword search End------")

    end_time = time.time()
    execution_time = end_time - start_time

    loginfo = f'Keyword search total Time: {execution_time} seconds, search {len(Y)} keyowrd(s) in {total_count*len(X)} keyowrd(s).'
    logging.info(loginfo)
    print(loginfo)
    loginfo = f'Avg. Keyword search Time: {execution_time/len(Y)} seconds, from total {total_count * len(X)} keyowrd(s).'
    logging.info(loginfo)
    print(loginfo)

if __name__ == '__main__':
    main()