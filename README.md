# variational-quantum-eigensolver

    # 2.2 Performance Analysis
    The custom variational circuit repeats a pattern, consisting of a single layer of parameterized U3 gates followed 
    by a linear chain of CX gates, thrice. Note that if the circuit operates on n qubits, there should be 3 ·(n−1) CX 
    gates, 3n U3 gates, and a total of 3 · 3 · n = 9n parameters. The circuit looks like the diagram bellow for 4 qubits. 
    This is a derivative of the circuit that was given to us. 
    
    However, note that tha parameters to the U3 gates aren't all zeros or even initialized to zeros. They only represent 
    the fact that they are parameters. The parameters are tuned by the optimizers just as in the given circuit and 
    are initialized to random values. 
    
        ┌───────────┐     ┌───────────┐                          ┌───────────┐                               ┌─┐
q_0: |0>┤ U3(0,0,0) ├──■──┤ U3(0,0,0) ├───────────────────■──────┤ U3(0,0,0) ├───────────────────■───────────┤M├──────────────
        ├───────────┤┌─┴─┐└───────────┘┌───────────┐    ┌─┴─┐    └───────────┘┌───────────┐    ┌─┴─┐         └╥┘     ┌─┐      
q_1: |0>┤ U3(0,0,0) ├┤ X ├──────■──────┤ U3(0,0,0) ├────┤ X ├──────────■──────┤ U3(0,0,0) ├────┤ X ├──────■───╫──────┤M├──────
        ├───────────┤└───┘    ┌─┴─┐    └───────────┘┌───┴───┴───┐    ┌─┴─┐    └───────────┘┌───┴───┴───┐┌─┴─┐ ║      └╥┘┌─┐   
q_2: |0>┤ U3(0,0,0) ├─────────┤ X ├──────────■──────┤ U3(0,0,0) ├────┤ X ├──────────■──────┤ U3(0,0,0) ├┤ X ├─╫───■───╫─┤M├───
        ├───────────┤         └───┘        ┌─┴─┐    ├───────────┤    └───┘        ┌─┴─┐    ├───────────┤└───┘ ║ ┌─┴─┐ ║ └╥┘┌─┐
q_3: |0>┤ U3(0,0,0) ├──────────────────────┤ X ├────┤ U3(0,0,0) ├─────────────────┤ X ├────┤ U3(0,0,0) ├──────╫─┤ X ├─╫──╫─┤M├
        └───────────┘                      └───┘    └───────────┘                 └───┘    └───────────┘      ║ └───┘ ║  ║ └╥┘
 c_0: 0 ══════════════════════════════════════════════════════════════════════════════════════════════════════╩═══════╬══╬══╬═
                                                                                                                      ║  ║  ║ 
 c_1: 0 ══════════════════════════════════════════════════════════════════════════════════════════════════════════════╩══╬══╬═
                                                                                                                         ║  ║ 
 c_2: 0 ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╩══╬═
                                                                                                                            ║ 
 c_3: 0 ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╩═
                                                                            
    
              
    In terms of finding the optimal solution, it performed almost as well as the circuit that was given to us in most 
    cases. There were some cases where it performed worse, however, if we conducted more test with different optimizers
    it may perform better since it has more parameters. For a particular IndependentSet problem that required 8 qubits, 
    the custom circuit consistently performed better. Although, as before, this could be caused by randomness from 
    different parts of the algorithm. Since each optimization took a significant amount of time for the custom circuit, 
    I wasn't able to conduct enough tests to get statistically significant results. 
    
    In terms of time required for parameter optimization, the custom model consistently took longer. This can be 
    attributed to the increase in the number of parameters. 
