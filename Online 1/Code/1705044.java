import org.chocosolver.solver.Model;
import org.chocosolver.solver.Solver;
import org.chocosolver.solver.variables.IntVar;


public class kenduku {
public static void main(String[] args) {


int i, j, k;


// 1. Create a Model
Model model = new Model("Kenduku");
// 2. Create variables



/* the board which is 9 X 9 */
/* (0, 0) is the top left position and (8, 8) is the bottom right position */
IntVar[][] bd = model.intVarMatrix("bd", 6, 6, 1, 6);


IntVar m4 = model.intVar("m4", 1, 36);

// 3. Post constraints
// box 0
IntVar s0 = bd[0][0].sub(bd[0][1]).intVar();
model.absolute(model.intVar(1), s0).post();

// box 1
IntVar s1 = bd[0][2].sub(bd[0][3]).intVar();
model.absolute(model.intVar(2), s1).post();

// box 2
IntVar d2_1 = bd[0][4].div(bd[1][4]).intVar();
IntVar d2_2 = bd[1][4].div(bd[0][4]).intVar();
(d2_1.eq(2)).or(d2_2.eq(2)).post();


// box 3
model.times(bd[0][5], bd[1][5], 30).post();


// box 4
model.times(bd[1][0], bd[2][0], m4).post();
model.times(m4, bd[3][0], 120).post();


// box 5
model.sum(new IntVar[]{bd[1][1], bd[2][1]}, "=", 7).post();


// box 6
model.sum(new IntVar[]{bd[1][2], bd[1][3]}, "=", 6).post();

// box 7
model.times(bd[2][3], bd[3][3], 15).post();

// box 8
IntVar s8 = bd[2][4].sub(bd[3][4]).intVar();
model.absolute(model.intVar(1), s8).post();

// box 9
IntVar d9_1 = bd[2][5].div(bd[3][5]).intVar();
IntVar d9_2 = bd[3][5].div(bd[2][5]).intVar();
(d9_1.eq(2)).or(d9_2.eq(2)).post();

// box 10
model.sum(new IntVar[]{bd[5][0], bd[4][0], bd[5][1]}, "=", 9).post();


// box 11
model.sum(new IntVar[]{bd[4][1], bd[3][1]}, "=", 6).post();

// box 12
IntVar s12 = bd[4][2].sub(bd[4][3]).intVar();
model.absolute(model.intVar(1), s12).post();


// box 13
model.times(bd[5][2], bd[5][3], 4).post();

// box 14
IntVar s14 = bd[4][4].sub(bd[5][4]).intVar();
model.absolute(model.intVar(1), s14).post();

// box 15
model.times(bd[4][5], bd[5][5], 12).post();

// box 16
IntVar d16_1 = bd[2][2].div(bd[3][2]).intVar();
IntVar d16_2 = bd[3][2].div(bd[2][2]).intVar();
(d16_1.eq(3)).or(d16_2.eq(3)).post();

/* post constraints for the given hints or clues */


/* for the nine box variables */
/* each box variable is associated with appropriate cell positions in board */

    
    
/* for the nine row variables */
/* each row variable is associated with appropriate cell positions in board */


 // row constraints
 IntVar[] rows;

 for(i=0; i<6; i++){
     rows = new IntVar[6];
     for(j=0; j<6; j++){
         rows[j] = bd[i][j];
     }
     model.allDifferent(rows).post();
 }


 // col constraints
 IntVar[] cols;

 for(i=0; i<6; i++){
     cols = new IntVar[6];
     for( j=0; j<6; j++){
         cols[j] = bd[j][i];
     }
     model.allDifferent(cols).post();
 }

/* post global constraint alldiff for the nine boxes */




// 4. Solve the problem




     Solver solver = model.getSolver();

    solver.showStatistics();
    solver.showSolutions();
    solver.findSolution();


// 5. Print the solution

for ( i = 0; i < 6; i++)
    {
for ( j = 0; j < 6; j++)
     { 
  
        System.out.print(" "); 
        /* get the value for the board position [i][j] for the solved board */
        k = bd [i][j].getValue();
        System.out.print(k );
     }
     System.out.println();
    }


}

}
