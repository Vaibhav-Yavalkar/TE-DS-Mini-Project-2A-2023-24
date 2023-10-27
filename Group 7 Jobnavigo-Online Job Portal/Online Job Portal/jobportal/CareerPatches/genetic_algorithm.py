import random

# Constants representing jobs and their required skills
JOBS = ['Software Developer', 'Data Analyst', 'Graphic Designer', 'Project Manager', 'Marketing Specialist']
JOBS_REQUIRED_SKILLS = {
    'Software Developer': ['Programming', 'Problem Solving', 'Web Development'],
    'Data Analyst': ['Data Analysis', 'Statistics', 'SQL'],
    'Graphic Designer': ['Graphic Design', 'Adobe Creative Suite'],
    'Project Manager': ['Project Management', 'Leadership', 'Communication'],
    'Marketing Specialist': ['Marketing', 'Social Media', 'Content Creation']
}

# Mapping of broader goals to required skills
BROADER_GOALS_TO_SKILLS = {
    'get_hired': ['Programming', 'Problem Solving', 'Communication'],
    'career_change': ['Transferable Skills', 'Networking', 'Adaptability']
}

# Parameters for the genetic algorithm
POPULATION_SIZE = 10
MUTATION_RATE = 0.1
NUM_GENERATIONS = 20
NUM_JOBS_TO_RECOMMEND = 3  # Define the number of jobs to recommend

def generate_chromosome():
    """Generate a random binary chromosome representing job selection."""
    return [random.choice([0, 1]) for _ in range(len(JOBS))]

def fitness(chromosome, user_goals, skills):
    """Fitness function based on user preferences, goals, and skills."""
    # Count the number of desired skills targeted
    targeted_skills = []
    for i in range(len(JOBS)):
        if chromosome[i] == 1:
            targeted_skills.extend(JOBS_REQUIRED_SKILLS[JOBS[i]])

    # Count the number of skills aligned with the user's broader goals
    targeted_desired_skills = sum(
        1 for skill in targeted_skills if skill in user_goals)

    # Consider user's skills in fitness calculation
    # You can add specific logic based on user's skills here

    return targeted_desired_skills

def get_user_goals():
    """Get user's job goals and skills as input."""
    print("Please choose your job goal:")
    print("1. Get Hired")
    print("2. Career Change")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        user_goals = BROADER_GOALS_TO_SKILLS['get_hired']
    elif choice == '2':
        user_goals = BROADER_GOALS_TO_SKILLS['career_change']
    else:
        print("Invalid choice. Using default goal: Get Hired")
        user_goals = BROADER_GOALS_TO_SKILLS['get_hired']

    # Get user's skills
    skills = input("Please enter your skills (comma-separated, e.g., Programming,Communication): ").strip().split(',')
    skills = [skill.strip() for skill in skills]

    return user_goals, skills

def genetic_algorithm(user_goals, skills):
    """Genetic algorithm to recommend jobs based on user goals and skills."""
    # Initialize the population
    population = [generate_chromosome() for _ in range(POPULATION_SIZE)]

    for generation in range(NUM_GENERATIONS):
        # Evaluate fitness of each chromosome
        fitness_scores = [fitness(chromosome, user_goals, skills) for chromosome in population]

        # Rest of the genetic algorithm steps remain the same

    # Recommend the best set of jobs after all generations
    best_chromosome = population[fitness_scores.index(max(fitness_scores))]
    recommended_jobs = [JOBS[i] for i in range(len(JOBS)) if best_chromosome[i]]
    
    return recommended_jobs  # Move the return statement here


