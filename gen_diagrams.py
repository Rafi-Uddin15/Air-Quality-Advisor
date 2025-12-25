import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_wiring_diagram():
    fig, ax = plt.figure(figsize=(10, 6)), plt.gca()
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.axis('off')
    
    # Title
    ax.text(50, 58, 'System Wiring Diagram', ha='center', fontsize=16, weight='bold')

    # Styles
    box_props = dict(boxstyle="round,pad=1", ec="#333", fc="#f0f0f0", lw=2)
    wire_props = dict(arrowstyle="-", color="#d32f2f", lw=2) # Red 5V
    gnd_props = dict(arrowstyle="-", color="#1976d2", lw=2)  # Blue GND
    data_props = dict(arrowstyle="-", color="#388e3c", lw=2) # Green Data

    # 1. Arduino (Center)
    ax.text(50, 30, "Arduino Uno R3\n(Controller)", ha='center', va='center', bbox=dict(boxstyle="round,pad=2", fc="#00979d", ec="black", alpha=0.3))
    
    # 2. DHT11 (Left)
    ax.text(15, 30, "DHT11 Sensor\n(Temp/Hum)", ha='center', va='center', bbox=box_props)
    
    # 3. MQ-135 (Right)
    ax.text(85, 30, "MQ-135 Sensor\n(Gas/Air)", ha='center', va='center', bbox=box_props)

    # Wires: 5V (Red)
    ax.annotate("", xy=(50, 35), xytext=(50, 45), arrowprops=wire_props) # Arduino to Rail
    ax.text(50, 46, "5V Rail (Red)", ha='center', color="#d32f2f", weight='bold')
    
    ax.annotate("", xy=(15, 35), xytext=(50, 45), arrowprops=dict(arrowstyle="-", color="#d32f2f", lw=2, connectionstyle="angle,angleA=0,angleB=90,rad=10")) # DHT to Rail
    ax.annotate("", xy=(85, 35), xytext=(50, 45), arrowprops=dict(arrowstyle="-", color="#d32f2f", lw=2, connectionstyle="angle,angleA=0,angleB=90,rad=10")) # MQ to Rail

    # Wires: GND (Blue)
    ax.annotate("", xy=(50, 25), xytext=(50, 15), arrowprops=gnd_props) # Arduino to Rail
    ax.text(50, 14, "GND Rail (Blue)", ha='center', color="#1976d2", weight='bold')

    ax.annotate("", xy=(15, 25), xytext=(50, 15), arrowprops=dict(arrowstyle="-", color="#1976d2", lw=2, connectionstyle="angle,angleA=0,angleB=-90,rad=10")) # DHT to Rail
    ax.annotate("", xy=(85, 25), xytext=(50, 15), arrowprops=dict(arrowstyle="-", color="#1976d2", lw=2, connectionstyle="angle,angleA=0,angleB=-90,rad=10")) # MQ to Rail

    # Wires: Data (Green)
    ax.annotate("Pin D2", xy=(25, 30), xytext=(40, 30), arrowprops=dict(arrowstyle="->", color="#388e3c", lw=2)) 
    ax.annotate("Pin A0", xy=(75, 30), xytext=(60, 30), arrowprops=dict(arrowstyle="->", color="orange", lw=2))

    plt.tight_layout()
    plt.savefig('docs/images/diagram_wiring.png', dpi=100)
    plt.close()

def create_methodology_flowchart():
    fig, ax = plt.figure(figsize=(8, 10)), plt.gca()
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title
    ax.text(50, 95, 'Project Methodology & Data Flow', ha='center', fontsize=16, weight='bold')

    # Draw Boxes
    blocks = [
        (90, "1. Sensing Layer\nDHT11 & MQ-135 convert physics to signals"),
        (75, "2. Acquisition Layer\nArduino Uno reads & serializes data"),
        (60, "3. Transmission Layer\nUSB Serial (COM Port) @ 9600 baud"),
        (45, "4. Data Processing Layer\nPython Logger saves CSV to Disk"),
        (30, "5. Intelligence Layer\nRandom Forest Model Predicts AQI"),
        (15, "6. Presentation Layer\nStreamlit Dashboard (RAG Advice)")
    ]

    for y, text in blocks:
        ax.text(50, y, text, ha='center', va='center', 
                bbox=dict(boxstyle="round,pad=1.5", fc="white", ec="#007bff", lw=2),
                fontsize=11)
        
        # Arrow down
        if y > 15:
            ax.annotate("", xy=(50, y-6), xytext=(50, y-3), arrowprops=dict(arrowstyle="->", lw=2, color="#555"))

    plt.tight_layout()
    plt.savefig('docs/images/diagram_methodology.png', dpi=100)
    plt.close()

if __name__ == "__main__":
    create_wiring_diagram()
    create_methodology_flowchart()
    print("Diagrams generated successfully.")
