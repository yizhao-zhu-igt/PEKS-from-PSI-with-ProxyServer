# Efficient Public-key Searchable Encryption Scheme from PSI with Scalable Proxy Servers
Efficient Public-key Searchable Encryption Scheme from PSI with Scalable Proxy Servers
## Description

This project is a simulation of an Efficient Public-key Searchable Encryption Scheme that utilizes Private Set Intersection (PSI) with Scalable Proxy Servers. The simulation involves the following steps:

1. Data generation: The `0_DataGen.py` script generates the test data for the keywords, including the data owner's keyword sets and the data user's keyword set.
2. Setup: The `1_Setup.py` script sets up the public parameters for the encryption scheme.
3. Token and ciphertext generation: The `2_Token_And_Ciper_Gen_OPRF` script generates the keyword search tokens and ciphertext.
4. Cloud server pre-processing: The `3_ClouldServer_Pre_Processing` script completes the pre-processing on the cloud server side.
5. Keyword search: The `4_Keyword_Search_PSI` script simulates the keyword search using the generated tokens within the ciphertexts.

The simulation output logs the various steps and timings of the process, providing insights into the performance and efficiency of the encryption scheme.

## Dependencies

This project requires the following dependencies:
- Python 3.x
- Cryptography library
- NumPy library



## Samples of excution Logs


**Execute 0_DataGen.py**
<pre>
2024-08-16 00:34:29 Data owner - Set Num: 10
2024-08-16 00:34:29 Keywords Per Set (Data owner): 100
2024-08-16 00:34:29 Data owner: Search Keywords Number: 10
2024-08-16 00:34:29 Data Owner Keywords: 1000 In Total - generated
2024-08-16 00:34:29 Data User Keywords: 10 In Total - generated
2024-08-16 00:34:29 Data owner keywords Set saved to file: do_keyword_sets.json
2024-08-16 00:34:29 Data user keywords Set saved to file: du_keyword_set.json
</pre>

**1_Setup.py**
<pre>
2024-08-16 00:35:05 randgen: <random.SystemRandom object at 0x0000019724FD97F0>
2024-08-16 00:35:05 security_parameter_bits: 256
2024-08-16 00:35:05 -----------setup() start---------------------
2024-08-16 00:35:05 -----------setup() end----------------------
2024-08-16 00:35:05 Setup Time: 0.02602076530456543 seconds
2024-08-16 00:35:05 Setup Time: 26.02076530456543 millisecond
2024-08-16 00:35:05 Save public parameters to the file: public_params.json
2024-08-16 00:35:05 Public parameters [p]: 86677805048572020991788572780328597329739912893470580178702096293082288202859
2024-08-16 00:35:05 Public parameters [q]: 43338902524286010495894286390164298664869956446735290089351048146541144101429
2024-08-16 00:35:05 Public parameters [g]: 19297527285066529265454609697033848751256679366102005973503197331787333292451
2024-08-16 00:35:05 Public parameters [h]: 7447314927951270772763710799525122921468655847693100588234688199011709695511
</pre>

**2_Token_And_Ciper_Gen_OPRF.py**
<pre>
2024-08-16 00:35:10 ------Token and CiperText Generation Start------
2024-08-16 00:35:10 Load Data Owner file: do_keyword_sets.json
2024-08-16 00:35:10 Load Data User file: du_keyword_set.json
2024-08-16 00:35:10 Save Token into file Y.json
2024-08-16 00:35:11 ------Token and CiperText Generation End------
2024-08-16 00:35:11 Save Ciper Text into file X_star.json
2024-08-16 00:35:11 Save Token into file Y.json
2024-08-16 00:35:11 Token Generation Total Time\uff1a0.01602005958557129 seconds, Generated 10 Token(s).
2024-08-16 00:35:11 Token Generation Avg. Time\uff1a0.001602005958557129 seconds.
2024-08-16 00:35:11 Token Generation Total Time\uff1a0.1560063362121582 seconds, Generated 1000 CiperText(s).
2024-08-16 00:35:11 Token Generation Avg. Time\uff1a0.0001560063362121582 seconds.
</pre>

**3_ClouldServer_Pre_Processing.py**
<pre>
2024-08-16 00:35:16 ------Cloud Server Pre-processing Start------
2024-08-16 00:35:16 Save search_parameters K_1 and a_coeffs into ps_1_data.json
2024-08-16 00:35:16 Save search_parameters K_2 and a_coeffs into ps_2_data.json
2024-08-16 00:35:16 Save search_parameters K_3 and a_coeffs into ps_3_data.json
2024-08-16 00:35:16 Save search_parameters K_4 and a_coeffs into ps_4_data.json
2024-08-16 00:35:16 Save search_parameters K_5 and a_coeffs into ps_5_data.json
2024-08-16 00:35:16 Save search_parameters K_6 and a_coeffs into ps_6_data.json
2024-08-16 00:35:16 Save search_parameters K_7 and a_coeffs into ps_7_data.json
2024-08-16 00:35:16 Save search_parameters K_8 and a_coeffs into ps_8_data.json
2024-08-16 00:35:16 Save search_parameters K_9 and a_coeffs into ps_9_data.json
2024-08-16 00:35:16 Save search_parameters K_10 and a_coeffs into ps_10_data.json
2024-08-16 00:35:16 ------Cloud Server Pre-processing End------
2024-08-16 00:35:16 Clould Server Pre Processing Total\uff1a0.1886434555053711 seconds, geneated 10 polynomials with degress 100
2024-08-16 00:35:16 Avg. polynomial interperation time\uff1a0.01886434555053711 seconds

**4_Keyword_Search_PSI.py** 
<pre>
2024-08-16 00:36:27 Found file: ps_10_data.json
2024-08-16 00:36:27 Found file: ps_1_data.json
2024-08-16 00:36:27 Found file: ps_2_data.json
2024-08-16 00:36:27 Found file: ps_3_data.json
2024-08-16 00:36:27 Found file: ps_4_data.json
2024-08-16 00:36:27 Found file: ps_5_data.json
2024-08-16 00:36:27 Found file: ps_6_data.json
2024-08-16 00:36:27 Found file: ps_7_data.json
2024-08-16 00:36:27 Found file: ps_8_data.json
2024-08-16 00:36:27 Found file: ps_9_data.json
2024-08-16 00:36:27 ------Keyword search Start------
2024-08-16 00:36:27 Load public params
2024-08-16 00:36:27 ------Load Y------
2024-08-16 00:36:27 Randomly Choose Proxy Server, Proxy Serer Index {random_ps_index}.
2024-08-16 00:36:27 Loading PS Data from ps_{random_ps_index}_data.json.
2024-08-16 00:36:27 Compute ct_j and t_j
2024-08-16 00:36:27 Perform keyword search
2024-08-16 00:36:27 ------Keyword search End------
2024-08-16 00:36:27 Keyword search total Time: 0.10758209228515625 seconds, search 10 keyowrd(s) in 1000 keyowrd(s).
2024-08-16 00:36:27 Avg. Keyword search Time: 0.010758209228515624 seconds, from total 1000 keyowrd(s).
</pre>
