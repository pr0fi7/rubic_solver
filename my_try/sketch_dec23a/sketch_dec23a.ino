// Define motor pins
#define PULL_RIGHT 22
#define DIR_RIGHT 23

#define PULL_DOWN 25
#define DIR_DOWN 24

#define PULL_LEFT 27
#define DIR_LEFT 26

#define PULL_TOP 29
#define DIR_TOP 28

#define PULL_FRONT 31
#define DIR_FRONT 30

#define PULL_BACK 33
#define DIR_BACK 32

#define STEP_DELAY 100  // Delay in microseconds

// Maximum number of commands in the queue
#define QUEUE_SIZE 300

// Struct to hold a single motor command
struct MotorCommand {
  String motor;
  String direction;
  int steps;
};

// Command queue
MotorCommand commandQueue[QUEUE_SIZE];
int queueSize = 0;  // Tracks the current size of the queue
int totalCommands = 0;  // Tracks the total number of commands to be received

// Function to add a command to the queue
bool enqueue(const MotorCommand& command) {
  if (queueSize >= QUEUE_SIZE) {
    Serial.println("Queue is full, cannot add command");
    return false;
  }
  commandQueue[queueSize] = command;
  queueSize++;
  return true;
}

// Function to remove a command from the queue
bool dequeue(MotorCommand& command) {
  if (queueSize == 0) {
    Serial.println("Queue is empty");
    return false;
  }
  command = commandQueue[0];
  for (int i = 1; i < queueSize; i++) {
    commandQueue[i - 1] = commandQueue[i];
  }
  queueSize--;
  return true;
}

// Function to rotate a motor
void rotateStepper(int pullPin, int dirPin, int steps, int direction) {
  digitalWrite(dirPin, direction);
  for (int i = 0; i < steps; i++) {
    digitalWrite(pullPin, HIGH);
    delayMicroseconds(STEP_DELAY);
    digitalWrite(pullPin, LOW);
    delayMicroseconds(STEP_DELAY);
  }
}

// Function to process a single command
void processCommand(const MotorCommand& command) {
  int pullPin, dirPin, dirSignal;

  // Map motor names to pins
  if (command.motor == "RIGHT") {
    pullPin = PULL_RIGHT;
    dirPin = DIR_RIGHT;
  } else if (command.motor == "LEFT") {
    pullPin = PULL_LEFT;
    dirPin = DIR_LEFT;
  } else if (command.motor == "TOP") {
    pullPin = PULL_TOP;
    dirPin = DIR_TOP;
  } else if (command.motor == "BOTTOM") {
    pullPin = PULL_DOWN;
    dirPin = DIR_DOWN;
  } else if (command.motor == "FRONT") {
    pullPin = PULL_FRONT;
    dirPin = DIR_FRONT;
  } else if (command.motor == "BACK") {
    pullPin = PULL_BACK;
    dirPin = DIR_BACK;
  } else {
    Serial.println("Invalid motor name");
    return;
  }

  // Map direction
  if (command.direction == "CW") {
    dirSignal = LOW;
  } else if (command.direction == "CnW") {
    dirSignal = HIGH;
  } else {
    Serial.println("Invalid direction");
    return;
  }

  // Execute the motor rotation
  rotateStepper(pullPin, dirPin, command.steps, dirSignal);
}

void setup() {
  Serial.begin(115200);
  pinMode(PULL_RIGHT, OUTPUT);
  pinMode(DIR_RIGHT, OUTPUT);
  pinMode(PULL_DOWN, OUTPUT);
  pinMode(DIR_DOWN, OUTPUT);
  pinMode(PULL_LEFT, OUTPUT);
  pinMode(DIR_LEFT, OUTPUT);
  pinMode(PULL_TOP, OUTPUT);
  pinMode(DIR_TOP, OUTPUT);
  pinMode(PULL_FRONT, OUTPUT);
  pinMode(DIR_FRONT, OUTPUT);
  pinMode(PULL_BACK, OUTPUT);
  pinMode(DIR_BACK, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    // If the total number of commands has not been received yet
    if (totalCommands == 0) {
      totalCommands = Serial.readStringUntil('\n').toInt();  // Read the number of commands
      queueSize = 0;  // Reset the queue size
      Serial.println("OK");
      return;
    }

    // Process incoming commands
    String input = Serial.readStringUntil('\n');
    input.trim();

    int comma1 = input.indexOf(',');
    int comma2 = input.indexOf(',', comma1 + 1);

    if (comma1 == -1 || comma2 == -1) {
      Serial.println("Invalid command format");
      return;
    }

    MotorCommand command;
    command.motor = input.substring(0, comma1);
    command.direction = input.substring(comma1 + 1, comma2);
    command.steps = input.substring(comma2 + 1).toInt();

    if (enqueue(command)) {
      Serial.println("OK");
    }

    // Once all commands are received, process the queue
    if (queueSize == totalCommands) {
      while (queueSize > 0) {
        MotorCommand cmd;
        if (dequeue(cmd)) {
          processCommand(cmd);
          Serial.println("OK");
        }
      }
      totalCommands = 0;  // Reset for the next batch of commands
    }
  }
}
