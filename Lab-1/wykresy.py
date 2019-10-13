import matplotlib.pyplot as plt
import statistics as stat

list_of_files = ['rsel.csv', '1-Evol-RS', 'b', 'o', 'cel-rs.csv', '1-Coev-RS', 'g', 'v',
                 '2cel-rs.csv', '2-Coev-RS', 'r', 'D', 'cel.csv', '1-Coev', 'k', 's',
                 '2cel.csv', '2-Coev', 'm', 'd']

fig, ax = plt.subplots(ncols=2)
fig.set_figheight(6.7)
fig.set_figwidth(8.0)
x_final_axis = []
means = []

for i in range(int(len(list_of_files) / 4)):
    x_axis = []
    y_axis = []

    file = open(list_of_files[4 * i])
    file.readline()

    for j in range(200):
        temp_vals = file.readline().split(',')
        values = temp_vals[2:-1]
        values.append(temp_vals[-1][0:-1])

        for k in range(len(values)):
            values[k] = float(values[k])
        y_axis.append(stat.mean(values))
        x_axis.append(temp_vals[1])
        if j == 199:
            means.append(values)

    if i == 0:
        x_final_axis = x_axis
    ax[0].plot(x_final_axis, y_axis, marker=list_of_files[4 * i + 3], markevery=25, markeredgecolor='k',
               markeredgewidth=0.5, label=list_of_files[4 * i + 1], color=list_of_files[4 * i + 2], linewidth=1)

    file.close()

ax[0].set_ylim(0.6, 1.0)
ax[0].set_yticklabels([60, 65, 70, 75, 80, 85, 90, 95, 100], fontname='serif', fontsize=9)
ax[0].set_ylabel("Odsetek wygranych gier[%]")

ax[0].set_xticks([0, 40, 80, 120, 160, 200])
ax[0].set_xlim(0, 200)
ax[0].set_xticklabels([0, 100, 200, 300, 400, 500], fontname='serif', fontsize=9)
ax[0].set_xlabel("Rozegranych gier (x1000)", fontname='serif', fontsize=9)

ax[0].legend(numpoints=2)
ax[0].grid(linestyle=':', linewidth=1.2)

ax2 = ax[0].twiny()
ax2.set_xticklabels([0, 40, 80, 120, 160, 200], fontname='serif', fontsize=9)
ax2.set_xlabel("Pokolenie", fontname='serif', fontsize=9)

ax[1].boxplot(means, showmeans=True, notch=True,
              meanprops=dict(marker='o', markerfacecolor='b', markeredgecolor='k', markersize=5),
              boxprops=dict(color='b', linewidth=1.2),
              whiskerprops=dict(color='b', linestyle='-.', linewidth=1.1),
              flierprops=dict(marker='+', markeredgecolor='b'),
              medianprops=dict(color='r'))
ax[1].grid(linestyle=':', linewidth=1.2)
ax[1].yaxis.tick_right()
ax[1].set_ylim(0.6, 1.0)
ax[1].set_yticklabels([60, 65, 70, 75, 80, 85, 90, 95, 100], fontname='serif', fontsize=9)
ax[1].set_xticklabels(['1-Evol-RS', '1-Coev-RS', '2-Coev-RS', '1-Coev', '2-Coev'], rotation=20,
                      fontname='serif', fontsize=9)

fig.suptitle("Wizualizacja na 5.0", fontname='serif')
plt.savefig('wykresy.pdf')
plt.show()
