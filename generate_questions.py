generate_questions_prompt = """
Based on the given instructional playbook create 30 questions. Each question should be categorised into "Easy", "Medium" or "Hard" by level of difficulty. You can ask for 5 types of questions - True/False (TF), Multiple Choice Question (MCQ) (single answer correct), Multiple Answer Questions (MAQ) (more than one answer correct), Fill in the blanks (FITB) and Numerical Questions (NUMERICAL). Generate 6 of each type.  And in each type generate 2 Easy, 2 Medium and 2 Hard. Also mention the answer along with the questions.
Follow this format for generating the questions.
[{
    "question": "Question or statement or Fill in the black with blanks",
    "options": ["A. Option1", "B. Option2", ...], (Only applicable for MCQs)
    "answer": ["Answers or Fill In the Blank value"], (List in case of Multiple Answers),
    "difficulty": "Easy/Medium/Hard",
    "type":"TF OR MCQ OR MAQ OR FITB OR NUMERICAL" 
}]

===================
Playbook
===================
## Introduction

Mechanics is a crucial branch of physics that explores the behavior of physical bodies influenced by forces or displacements and their effects on the environment. This playbook dives into mechanics' foundational and advanced topics, illustrating its principles and how they apply to the real world.

## Key Concepts:

### 1. Historical Background
Mechanics has evolved from ancient civilizations to the modern era, with significant contributions from Aristotle, Archimedes, Galileo Galilei, Johannes Kepler, and Isaac Newton. These developments laid the groundwork for classical mechanics and its further subdivisions.

### 2. Branches of Mechanics
It splits mainly into classical and quantum mechanics, with classical mechanics further divided into kinematics, dynamics, statics, fluid mechanics, and continuum mechanics.

### 3. Fundamental Concepts
Discussing space, time, mass, inertia, force, energy, and momentum, these principles are central to understanding motion and forces in mechanics.

### 4. Importance of Mechanics
Mechanics is foundational in engineering, astronomy, biology, and everyday life, providing insight into the behavior of physical systems.

### 5. Mathematical Tools
Mathematics, specifically calculus, vectors, differential equations, and linear algebra, is essential for analyzing and describing the principles of mechanics.

### 6. Experimental and Theoretical Approaches
Mechanics utilizes both experimental data to observe physical phenomena and theoretical models to predict behaviors.

### 7. Modern Developments
Modern physics has extended mechanics to include relativistic and quantum realms, offering deeper understanding beyond classical mechanics' scope.

## Chapter Contributions

This chapter provides an in-depth foundation in the principles of mechanics. Through historical perspectives, fundamental concepts, and branches of mechanics, learners gain comprehensive knowledge essential for delving into more specialized and complex topics. It demonstrates the significant impact of mechanics on scientific advancements and technological development.

## Definitions and Examples

- **Kinematics**: Focuses on describing motion without considering the forces causing it. For example, calculating a car's velocity as it accelerates.
- **Dynamics**: Studies the forces causing motion, like determining the force needed to push a shopping cart.
- **Statics**: Examines forces in stationary systems, e.g., analyzing the forces acting on a bridge.
- **Fluid Mechanics**: Explores the behavior of fluids, such as understanding water flow in pipes.
- **Continuum Mechanics**: Deals with materials modeled as a continuous mass, analyzing stress and strain in engineering materials.

## Importance and Application

Mechanics not only lays the groundwork for understanding natural phenomena but also drives innovation in technology, medicine, and construction. It helps engineers design safer buildings, allows astronomers to explore the cosmos, and aids biologists in understanding human motion.

## Conclusion

The study of mechanics is fundamental to physics, encapsulating the understanding of the universe's physical laws. This chapter sets the stage for further exploration into advanced topics, highlighting mechanics' role as a cornerstone of scientific inquiry and technological progress."""