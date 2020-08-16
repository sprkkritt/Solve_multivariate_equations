import numpy as np
import matplotlib.pyplot as plt
import argparse

def FormatEq(cof):
    answer = cof[-1]
    cof = [str(x)+'x'+str(idx+1) for idx, x in enumerate(cof) if idx < len(cof)-1]
    cof_screen = ' + '.join(cof)
    cof_screen += ' = {}'.format(answer)
    print('-'*(len(cof_screen)+4))
    print('| {} |'.format(cof_screen))
    print('-'*(len(cof_screen)+4))

def Init_population(n, n_cof):
    pop = []
    for _ in range(n):
        chromosome = []
        for _ in range(n_cof):
            chromosome.append(np.random.randint(-1000,1000))
        pop.append(chromosome)
    return pop
            
    
def SolvEq(cof, n_chr, max_round = 1e+4): #chr -> chromosome , cof -> coefficient
    FormatEq(cof)
    cof = cof.split(',')
    n_chr = int(n_chr)
    cof = list(map(lambda x: int(x), cof))
    answer = cof[-1]
    len_cof = len(cof)-1
    pop = Init_population(n_chr,len_cof)
    mean_fitness = []

    #-----------------Start GENETIC Algorithm--------------------
    stop = False
    count_round = 0
    while not stop:
        fitness = []
        kill_point = n_chr // 2
        # selection
        for i in range(n_chr):
            func_obj = 0
            for j in range(len_cof):
                func_obj += cof[j]*pop[i][j]
            fitness.append(1/(1+abs(func_obj-answer)))
        mean_fitness.append(sum(fitness)/n_chr)
        fitness_idx = np.array(fitness).argsort()[::-1]

        best_fitness = round(fitness[fitness_idx[0]], 5)
        best_chromosome = pop[fitness_idx[0]]
        print('round : {}'.format(count_round))
        print('fitness : {} \nchromosome : {}'.format(best_fitness, best_chromosome))
        print('-'*45)
        if best_fitness >= 0.98:
            stop = True
            format_ans = ['x'+str(idx+1) + ' = ' + str(x) + '  ' for idx, x in enumerate(best_chromosome)]
            format_ans = ' '.join(format_ans)
            print('\n'+'-'*55)
            FormatEq(cof)
            print(' FINISH AT ROUND : {}'.format(count_round))
            print(' SOLUTION : {}\n'.format(best_chromosome))
            print(' {}'.format(format_ans))
            print('-'*55)
        
        #cross over
        if kill_point % 2 == 1:
            kill_point -= 1
        for i in range(kill_point,n_chr,2):
            cross_point = np.random.randint(0, len(pop[0]), size=2)
            #offspring1
            pop[i] = np.concatenate((pop[i][:cross_point[0]], pop[i+1][cross_point[0]:] ))
            #offspring2
            pop[i+1] = np.concatenate((pop[i+1][:cross_point[1]], pop[i][cross_point[1]:] ))

        
        #Mutation
        for i in range(1, n_chr):
            val = np.random.randint(-10,10)
            pos = np.random.randint(0,len_cof)
            pop[i][pos] = val

        count_round +=1
        if count_round == max_round:
            stop = True
            print('\n','-'*15,'CAN NOT FIND SOLUTION','-'*15)
            print('OPTIMAL ANSWER : {}'.format(best_chromosome))
        pop = pop
    #plot graph mean fitness
    X = np.arange(len(mean_fitness))
    plt.plot(X, mean_fitness, label = 'mean fitness')
    plt.xlabel('ROUND')
    plt.ylabel('MEAN FITNESS')
    plt.legend(loc='upper left')
    plt.show()
    

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('-c', '--coefficient', required=True, help='Cofficient of equation, From x1, x2, x3,..., xn // Ex. 2,3,4,5 -> 2x1+3x2+4x3 = 5 // Ex. 2,3,40 -> 2x1+3x2 = 40 // Ex. " -3,2,3" -> -3x1+2x2 = 3 ')
    ap.add_argument('-p', '--population', required=True, help='number of chromosome in population ')
    ap.add_argument('-m', '--max_round', required=False, help='MAX ROUND to find answer  ')
    args = vars(ap.parse_args())
    SolvEq(args['coefficient'], args['population'])