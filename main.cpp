#include<iostream>
#include<conio.h>
#include<windows.h>
#include<vector>
#include<ctime>
using namespace std;

// Utility function to set the cursor position in the console
void setCursorPosition(int x, int y) {
    COORD coord;
    coord.X = x;
    coord.Y = y;
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), coord);
}

// Struct to represent coordinates (used for player, bullets, and enemies)
struct Coordinate {
    int x, y;
};

class Player {
private:
    Coordinate position;
    int screenWidth;

public:
    Player(int screenWidth, int screenHeight) : screenWidth(screenWidth) {
        position.x = screenWidth / 2;
        position.y = screenHeight - 2;
    }

    void draw() const {
        setCursorPosition(position.x, position.y);
        cout << "^";
    }

    void erase() const {
        setCursorPosition(position.x, position.y);
        cout << " ";
    }

    void moveLeft() {
        if (position.x > 1)
            position.x--;
    }

    void moveRight() {
        if (position.x < screenWidth - 2)
            position.x++;
    }

    Coordinate getPosition() const {
        return position;
    }
};

class BulletManager {
private:
    vector<Coordinate> bullets;

public:
    void shoot(const Coordinate& playerPos) {
        bullets.push_back({playerPos.x, playerPos.y - 1});
    }

    void move(vector<Coordinate>& enemies, int& score) {
        vector<Coordinate> updatedBullets;

        for (auto& bullet : bullets) {
            bullet.y--;
            bool hit = false;

            for (auto it = enemies.begin(); it != enemies.end(); ++it) {
                if (bullet.x == it->x && bullet.y == it->y) {
                    enemies.erase(it);
                    score += 10;
                    hit = true;
                    break;
                }
            }

            if (!hit && bullet.y > 0)
                updatedBullets.push_back(bullet);
        }

        bullets = updatedBullets;
    }

    void draw() const {
        for (auto& bullet : bullets) {
            setCursorPosition(bullet.x, bullet.y);
            cout << ".";
        }
    }
};

class EnemyManager {
private:
    vector<Coordinate> enemies;
    int screenWidth;
    int screenHeight;

public:
    EnemyManager(int screenWidth, int screenHeight) : screenWidth(screenWidth), screenHeight(screenHeight) {}

    void generate() {
        if (rand() % 100 < 5) {
            int enemyX = rand() % (screenWidth - 2) + 1;
            enemies.push_back({enemyX, 1});
        }
    }

    bool move(const Coordinate& playerPos) {
        vector<Coordinate> updatedEnemies;
        for (auto& enemy : enemies) {
            enemy.y++;

            if (enemy.x == playerPos.x && enemy.y == playerPos.y)
                return true; // Game over condition

            if (enemy.y < screenHeight - 1)
                updatedEnemies.push_back(enemy);
        }

        enemies = updatedEnemies;
        return false;
    }

    void draw() const {
        for (auto& enemy : enemies) {
            setCursorPosition(enemy.x, enemy.y);
            cout << "V";
        }
    }

    vector<Coordinate>& getEnemies() {
        return enemies;
    }
};

class SpaceShooterGame {
private:
    int width, height;
    int score;
    bool isGameRunning;
    Player player;
    BulletManager bulletManager;
    EnemyManager enemyManager;

public:
    SpaceShooterGame(int width, int height)
        : width(width), height(height), score(0), isGameRunning(true),
          player(width, height), enemyManager(width, height) {}

    void start() {
        setupConsole();

        displayInstructions();

        while (isGameRunning) {
            handleInput();
            update();
            render();
            Sleep(30);
            system("cls");
        }

        showGameOverScreen();
    }

private:
    void setupConsole() {
        system("mode con: lines=40 cols=40");

        // Hide cursor
        HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
        CONSOLE_CURSOR_INFO cursorInfo;
        GetConsoleCursorInfo(hConsole, &cursorInfo);
        cursorInfo.bVisible = FALSE;
        SetConsoleCursorInfo(hConsole, &cursorInfo);

        srand(static_cast<unsigned int>(time(0)));
    }

    void displayInstructions() {
        cout << "Instructions\n";
        cout << "************\n";
        cout << "1. Use Left and Right arrow keys to move\n";
        cout << "2. Press Spacebar to shoot\n";
        cout << "3. Press Esc to quit the game\n\n";
        system("pause");
    }

    void handleInput() {
        if (_kbhit()) {
            char ch = _getch();
            switch (ch) {
                case 75: player.moveLeft(); break; // Left arrow
                case 77: player.moveRight(); break; // Right arrow
                case ' ': bulletManager.shoot(player.getPosition()); break;
                case 27: isGameRunning = false; break; // Esc
            }
        }
    }

    void update() {
        player.erase();
        bulletManager.move(enemyManager.getEnemies(), score);
        if (enemyManager.move(player.getPosition()))
            isGameRunning = false;
        enemyManager.generate();
    }

    void render() const {
        player.draw();
        bulletManager.draw();
        enemyManager.draw();
    }

    void showGameOverScreen() const {
        setCursorPosition(width / 2 - 5, height / 2);
        cout << "Game Over! Score: " << score << endl;
    }
};

int main() {
    SpaceShooterGame game(40, 40);
    game.start();
    return 0;
}
