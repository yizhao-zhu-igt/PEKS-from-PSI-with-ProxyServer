import random
import math
import json
import time
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import logging
import os


# Set up logging file
log_file = '2_Token_And_Ciper_Gen_OPRF.log'
if os.path.exists(log_file):
    os.remove(log_file)
# Set up logging
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def H1(input_data, q, g):
    input_bytes = input_data.encode()

    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(input_bytes)
    hash_bytes = digest.finalize()

    hash_int = int.from_bytes(hash_bytes, byteorder='big')

    group_element = pow(g, hash_int, q)

    return group_element

def H2(group_element):
    # Hash G_q element to l-bit binary string
    group_bytes = group_element.to_bytes((group_element.bit_length() + 7) // 8, byteorder='big')
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(group_bytes)
    hash_bytes = digest.finalize()
    return hash_bytes[:32].hex()  # l=32*8=256

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def sample_Zq_star(q):
    while True:
        x = random.randint(2, q - 1)
        if egcd(x, q)[0] == 1 and egcd(x, q-1)[0] == 1:
            return x

def token_generation(W, q, g, alpha):
    s = len(W)
    Y_prime = {}
    for j in range(s):
        w_j = W[f"w_{j+1}"]
        y_prime_j = pow(H1(w_j, q, g), alpha, q)
        Y_prime[f"y_prime_{j+1}"] = y_prime_j
    return Y_prime

def token_generation_do(Y_prime, beta, q):
    s = len(Y_prime)
    Z = {}
    for j in range(s):
        y_prime_j = Y_prime[f"y_prime_{j+1}"]
        z_j = pow(y_prime_j, beta, q)
        Z[f"z_{j+1}"] = z_j
    return Z

def token_generation_du(Z, alpha, q):
    s = len(Z)
    Y = {}
    for j in range(s):
        z_j = Z[f"z_{j+1}"]
        alpha_inv = modinv(alpha, q-1)
        z_prime_j = pow(z_j, alpha_inv, q)
        y_j = H2(z_prime_j)
        Y[f"y_{j+1}"] = y_j
    return Y

def ciphertext_generation(W_star, beta, q, g):
    X_star = []
    for i in range(len(W_star)):
        W_i = W_star[f"W^({i+1})"]
        n_i = len(W_i)
        X_i = {}
        for u in range(n_i):
            w_u_i = W_i[f"w_{u+1}^({i+1})"]
            x_u_i = H2(pow(H1(w_u_i, q, g), beta, q))
            X_i[f"x_{u+1}^({i+1})"] = x_u_i
        X_star.append(X_i)
    return X_star

def main():
    logging.info(f"------Token and CiperText Generation Start------")
    #logging.info(f"Setup Time: {duration_ms} millisecond")
    #print(f"Setup Time: {duration} seconds")
    with open('public_params.json', 'r') as file:
        setup_results = json.load(file)
        p = setup_results['p']
        q = setup_results['q']
        g = setup_results['g']
        h = setup_results['h']
    logging.info(f"Load Data Owner file: do_keyword_sets.json")
    with open('do_keyword_sets.json', 'r') as file:
        W_star = json.load(file)
    logging.info(f"Load Data User file: du_keyword_set.json")
    with open('du_keyword_set.json', 'r') as file:
        W = json.load(file)

    # DU samples α_j
    alpha = sample_Zq_star(q)

    #logging.info(f"------Token Generation Started------")
    # DU: Token Generating
    start_time_token_generation = time.time()
    Y_prime = token_generation(W, q, g, alpha)
    #logging.info(f"------Token Generation End------")
    # DU send Y_prime to DO
    with open('Y_prime.json', 'w') as file:
        json.dump(Y_prime, file)

    # DO smples β
    beta = sample_Zq_star(q)

    # DO Token Generating
    Z = token_generation_do(Y_prime, beta, q)

    # DO send Z to DU
    with open('Z.json', 'w') as file:
        json.dump(Z, file)

    Y = token_generation_du(Z, alpha, q)
    end_time_token_generation = time.time()
    token_generation_time = end_time_token_generation - start_time_token_generation


    with open('Y.json', 'w') as file:
        json.dump(Y, file)
    logging.info(f"Save Token into file Y.json")

    start_time_ciphertext_generation = time.time()
    X_star = ciphertext_generation(W_star, beta, q, g)

    logging.info(f"------Token and CiperText Generation End------")
    end_time_ciphertext_generation = time.time()
    ciphertext_generation_time = end_time_ciphertext_generation - start_time_ciphertext_generation

    logging.info(f"Save Ciper Text into file X_star.json")
    with open('X_star.json', 'w') as file:
        json.dump(X_star, file)

    logging.info(f"Save Token into file Y.json")
    loginfo = f"Token Generation Total Time：{token_generation_time} seconds, Generated {len(Y)} Token(s)."
    logging.info(loginfo)
    print(loginfo)
    loginfo = f"Token Generation Avg. Time：{token_generation_time/len(Y)} seconds."
    logging.info(loginfo)
    print(loginfo)
    loginfo = f"Token Generation Total Time：{ciphertext_generation_time} seconds, Generated {(len(X_star) * len(X_star[0]))} CiperText(s)."
    logging.info(loginfo)
    print(loginfo)

    agv_ciper_time = ciphertext_generation_time/(len(X_star) * len(X_star[0]))
    loginfo = f"Token Generation Avg. Time：{agv_ciper_time} seconds."
    logging.info(loginfo)
    print(loginfo)

if __name__ == "__main__":
    main()