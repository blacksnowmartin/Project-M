require 'gosu'

class Dog
  attr_reader :x, :y, :color

  def initialize(x, y, color, name)
    @x = x
    @y = y
    @color = color
    @name = name
    @speed = 5
  end

  def move_left;  @x -= @speed if @x > 0; end
  def move_right; @x += @speed if @x < 750; end
  def move_up;    @y -= @speed if @y > 0; end
  def move_down;  @y += @speed if @y < 550; end

  def draw
    # Drawing a rectangle to represent the dog
    # In a real game, you'd use Gosu::Image.new to draw a dog sprite
    Gosu.draw_rect(@x, @y, 50, 40, @color)
  end
end

class DogGame < Gosu::Window
  def initialize
    super 800, 600
    self.caption = "Balika & Sinawa: The Great Treat Hunt"

    # Balika is the Black Dog (using a dark grey so he's visible on black backgrounds)
    @balika = Dog.new(200, 300, Gosu::Color::BLACK, "Balika")
    
    # Sinawa is the White Dog
    @sinawa = Dog.new(600, 300, Gosu::Color::WHITE, "Sinawa")
    
    @font = Gosu::Font.new(20)
  end

  def update
    # Balika Controls (WASD Keys)
    @balika.move_left  if Gosu.button_down?(Gosu::KB_A)
    @balika.move_right if Gosu.button_down?(Gosu::KB_D)
    @balika.move_up    if Gosu.button_down?(Gosu::KB_W)
    @balika.move_down  if Gosu.button_down?(Gosu::KB_S)

    # Sinawa Controls (Arrow Keys)
    @sinawa.move_left  if Gosu.button_down?(Gosu::KB_LEFT)
    @sinawa.move_right if Gosu.button_down?(Gosu::KB_RIGHT)
    @sinawa.move_up    if Gosu.button_down?(Gosu::KB_UP)
    @sinawa.move_down  if Gosu.button_down?(Gosu::KB_DOWN)
  end

  def draw
    # Draw a green grass background
    Gosu.draw_rect(0, 0, 800, 600, Gosu::Color.rgb(50, 150, 50))
    
    @balika.draw
    @sinawa.draw

    @font.draw_text("Balika (WASD)", @balika.x - 10, @balika.y - 25, 1, 1, 1, Gosu::Color::BLACK)
    @font.draw_text("Sinawa (Arrows)", @sinawa.x - 10, @sinawa.y - 25, 1, 1, 1, Gosu::Color::WHITE)
    @font.draw_text("Find the treats!", 10, 10, 1, 1, 1, Gosu::Color::YELLOW)
  end
end

DogGame.new.show